import json
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .redis_client import redis_instance
from django.contrib.auth import get_user_model

User = get_user_model()

class SendMessageView(APIView):
    def post(self, request):
        """
        {
            "from_user_id": <int>,
            "to_user_id": <int>,
            "message": "<string>"
        }
        """
        data = request.data
        required_fields = ['from_user_id', 'to_user_id', 'message']
        if not all(field in data for field in required_fields):
            return Response({"error": "Campos 'from_user_id', 'to_user_id' e 'message' são obrigatórios."}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            from_user = User.objects.get(id=data['from_user_id'])
            to_user = User.objects.get(id=data['to_user_id'])
        except User.DoesNotExist:
            return Response({"error": "Usuário não encontrado."}, status=status.HTTP_404_NOT_FOUND)
        
        message_data = {
            "from_user_id": data['from_user_id'],
            "to_user_id": data['to_user_id'],
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
