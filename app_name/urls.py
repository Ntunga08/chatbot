from django.urls import path
from . import views

urlpatterns = [
    path('', views.chat_interface, name='chat_interface'),
    path('api/chat/', views.chat, name='chat'),
    path('api/chat/with-context/', views.chat_with_context, name='chat_with_context'),
    path('api/health/', views.health_check, name='health_check'),
] 