from django.urls import path
from . import views

urlpatterns = [
    path('interface/', views.interface_view, name='interface'),
    path('create-session/<int:ai_id>/', views.create_session, name='create_session'),
    path('chat/<int:session_id>/', views.chat_with_ai, name='chat_with_ai'),
]