import json
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from ..redis_client import redis_instance
from django.contrib.auth import get_user_model
from rest_framework.permissions import IsAuthenticated

User = get_user_model()

class SendMessageView(APIView):
    permission_classes = [IsAuthenticated]  
    def post(self, request):
        """
        {
            "to_user_id": <int>,
            "message": "<string>"
        }
        """
        data = request.data
        required_fields = ['to_user_id', 'message']

        if not all(field in data for field in required_fields):
            return Response(
                {"error": "Campos 'to_user_id' e 'message' são obrigatórios."}, 
                status=status.HTTP_400_BAD_REQUEST
            )

        from_user = request.user  
        try:
            to_user = User.objects.get(id=data['to_user_id'])
        except User.DoesNotExist:
            return Response({"error": "Usuário destinatário não encontrado."}, status=status.HTTP_404_NOT_FOUND)

        message_data = {
            "from_user_id": from_user.id,
            "to_user_id": to_user.id,
            "message": data['message']
        }

        try:
            redis_instance.publish('chat_messages', json.dumps(message_data))
            return Response({
                "status": "Mensagem enviada com sucesso.",
                "from_user": {
                    "id": from_user.id,
                    "username": from_user.username
                },
                "to_user": {
                    "id": to_user.id,
                    "username": to_user.username
                },
                "message": data['message']
            }, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": f"Erro ao publicar a mensagem: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
