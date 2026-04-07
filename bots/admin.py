from django.contrib import admin
from .models import AIConfig, ChatSession, ChatMessage # <-- Importações corrigidas aqui

@admin.register(AIConfig)
class AIConfigAdmin(admin.ModelAdmin):
    list_display = ('name', 'model_name', 'provider_url')
    search_fields = ('name',)
    fieldsets = (
        ('Identificação', {
            'fields': ('name',)
        }),
        ('Configurações da API', {
            'fields': ('provider_url', 'model_name', 'api_key')
        }),
        ('Personalidade e Memórias', {
            'fields': ('system_prompt', 'temperature', 'max_tokens'),
        }),
    )

class ChatMessageInline(admin.TabularInline):
    model = ChatMessage
    extra = 0
    readonly_fields = ('timestamp', 'role', 'content')
    can_delete = False

@admin.register(ChatSession)
class ChatSessionAdmin(admin.ModelAdmin):
    list_display = ('id', 'ai_config', 'created_at')
    list_filter = ('ai_config', 'created_at')
    inlines = [ChatMessageInline]