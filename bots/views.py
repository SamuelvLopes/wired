import json
import requests
import logging # <-- Importante
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
from .models import AIConfig, ChatSession, ChatMessage
from django.http import JsonResponse, StreamingHttpResponse # <-- Importe o StreamingHttpResponse
# Isso cria o logger com o nome 'bots.views', que o settings.py agora escuta
logger = logging.getLogger(__name__) 

# ... resto do seu código ...
# bots/views.py (ajuste na interface_view)
def interface_view(request):
    ais = AIConfig.objects.all()
    
    # Cria um dicionário para o JS mapear { "lain": 1, "pirata": 2 }
    ai_map = {ai.name.lower(): ai.id for ai in ais}
    
    return render(request, 'bots/interface.html', {
        'ais': ais,
        'ai_map_json': json.dumps(ai_map) # Passa como JSON para o template
    })
@csrf_exempt
def chat_with_ai(request, session_id):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            user_text = data.get('message', '')
            
            session = ChatSession.objects.get(id=session_id)
            config = session.ai_config

            if user_text:
                ChatMessage.objects.create(session=session, role='user', content=user_text)

            history = ChatMessage.objects.filter(session=session).order_by('timestamp')
            messages_payload = [{"role": "system", "content": config.system_prompt}]
            for msg in history:
                messages_payload.append({"role": msg.role, "content": msg.content})

            payload = {
                "model": config.model_name,
                "messages": messages_payload,
                "temperature": config.temperature,
                "stream": True 
            }

            headers = {"Content-Type": "application/json"}
            
            # --- FUNÇÃO GERADORA ROBUSTA ---
            def stream_generator():
                full_reply = ""
                try:
                    # Timeout curto para conexão, mas longo para leitura (streaming demora)
                    with requests.post(config.provider_url, json=payload, headers=headers, stream=True, timeout=(5, 60)) as r:
                        r.raise_for_status()
                        
                        for line in r.iter_lines():
                            if line:
                                # Decodifica e limpa a linha
                                decoded_line = line.decode('utf-8').strip()
                                
                                # SEGURANÇA: Só tenta dar load se parecer um JSON
                                if decoded_line.startswith('{'):
                                    try:
                                        chunk_json = json.loads(decoded_line)
                                        # Na rota /api/chat o conteúdo vem em message['content']
                                        if "message" in chunk_json:
                                            content = chunk_json["message"].get("content", "")
                                            full_reply += content
                                            yield json.dumps({"ai": config.name, "chunk": content}) + "\n"
                                        
                                        # O Ollama envia done: true no último chunk
                                        if chunk_json.get("done"):
                                            break
                                    except json.JSONDecodeError:
                                        continue
                                
                    if full_reply:
                        ChatMessage.objects.create(session=session, role='assistant', content=full_reply)
                        
                except Exception as stream_err:
                    logger.error(f"ERRO DE TRANSMISSÃO WIRED: {str(stream_err)}")
                    yield json.dumps({"ai": "SISTEMA", "chunk": f" [CONEXÃO INTERROMPIDA]: {str(stream_err)}"}) + "\n"

            response = StreamingHttpResponse(stream_generator(), content_type='application/x-ndjson')
            # Headers essenciais para evitar que o navegador faça cache do stream
            response['X-Accel-Buffering'] = 'no' 
            response['Cache-Control'] = 'no-cache'
            return response

        except Exception as e:
            logger.error(f"FALHA NA REQUISIÇÃO: {str(e)}")
            return JsonResponse({'error': str(e)}, status=500)
@csrf_exempt
def create_session(request, ai_id):
    """ Endpoint para criar um novo chat ID ao clicar em uma IA """
    if request.method == 'POST':
        ai = AIConfig.objects.get(id=ai_id)
        session = ChatSession.objects.create(ai_config=ai)
        return JsonResponse({'session_id': session.id, 'ai_name': ai.name})