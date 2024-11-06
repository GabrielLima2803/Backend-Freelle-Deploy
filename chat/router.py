from django.urls import path
from chat.views.conversa import IniciarConversaView
from chat.views.sendMessage import SendMessageView

urlpatterns = [
    path('iniciar-conversa/', IniciarConversaView.as_view(), name='iniciar-conversa'),
    path('enviar-mensagem/', SendMessageView.as_view(), name='enviar-mensagem'),
]
