from django.db import models

class AIConfig(models.Model):
    name = models.CharField(max_length=100)
    provider_url = models.URLField()
    model_name = models.CharField(max_length=50)
    api_key = models.CharField(max_length=255)
    system_prompt = models.TextField()
    temperature = models.FloatField(default=0.7)
    max_tokens = models.IntegerField(default=500)

    def __str__(self):
        return self.name

class ChatSession(models.Model):
    ai_config = models.ForeignKey(AIConfig, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=200, default="Nova conexão na Wired")

    def __str__(self):
        return f"{self.ai_config.name} - {self.created_at}"

class ChatMessage(models.Model):
    session = models.ForeignKey(ChatSession, related_name='messages', on_delete=models.CASCADE)
    role = models.CharField(max_length=10, choices=[('user', 'User'), ('assistant', 'Assistant')])
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)