# 🕸️ Serial Experiments Lain: Protocol 07

> *"No matter where you are, everyone is always connected."*

Este projeto é uma interface de chat inspirada na estética de *Serial Experiments Lain*, focada na comunicação com múltiplas consciências (agentes de IA) através da **Wired**. O sistema utiliza **Django** como orquestrador e **Docker** para o processamento de modelos de linguagem locais (Ollama).

## 🛠️ Tecnologias e Protocolos

* **Backend:** Django 5.x (Python)
* **IA Engine:** Ollama via Docker (Llama3, Mistral, etc.)
* **Frontend:** Vanilla JS com estética CRT/Cyberpunk
* **Comunicação:** HTTP Streaming (NDJSON) para respostas em tempo real
* **Banco de Dados:** SQLite (Persistência de memória e logs de sessão)

## 📡 Funcionalidades

* **Multi-Agent Context:** Suporte para diferentes personalidades (Lain, L Detective, etc.).
* **Wired Streaming:** Respostas processadas e exibidas em tempo real (letra por letra).
* **Cross-Consciousness:** Menção de agentes usando `@` para roteamento entre IAs.
* **Persistent Memory:** Cada sessão de chat é salva no banco de dados.
* **Autocomplete:** Menu flutuante de menções inspirado em sistemas de terminais.

## 🚀 Como Executar

### 1. Preparar o Docker (Ollama)
```bash
docker run -d -v ollama:/root/.ollama -p 11434:11434 -e OLLAMA_HOST="0.0.0.0" --name ollama ollama/ollama
docker exec -it ollama ollama pull llama3
```

### 2. Configurar o django
```bash
python -m venv venv
source venv/bin/activate
pip install django requests python-dotenv
python manage.py migrate
python manage.py runserver 8085
```

Acesse em: http://127.0.0.1:8085/api/bots/interface/
---
Present Day, Present Time. Hahahaha!
