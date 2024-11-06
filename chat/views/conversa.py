from rest_framework.response import Response
from rest_framework.views import APIView
from django.db import models
from chat.models import Conversa  
from chat.serializers import ConversaSerializer

class IniciarConversaView(APIView):
    def post(self, request):
        usuario1 = request.user
        usuario2_id = request.data.get("usuario2_id")

        conversa = Conversa.objects.filter(
            (models.Q(usuario1_id=usuario1.id) & models.Q(usuario2_id=usuario2_id)) |
            (models.Q(usuario1_id=usuario2_id) & models.Q(usuario2_id=usuario1.id))
        ).first()

        if not conversa:
            conversa = Conversa.objects.create(usuario1=usuario1, usuario2_id=usuario2_id)

        return Response(ConversaSerializer(conversa).data)
