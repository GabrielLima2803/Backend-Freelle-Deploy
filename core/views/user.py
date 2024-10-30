from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from core.models import User, Avaliacao
from core.serializers import (
    UserSerializer, 
    UserListSerializer, 
    UserDetailSerializer,
    AvaliacaoSerializer
)

class UserViewSet(ModelViewSet):
    queryset = User.objects.all().order_by("id")
    serializer_class = UserSerializer

    @action(detail=False, methods=["get"], permission_classes=[IsAuthenticated])
    def me(self, request):
        """Return the current authenticated user"""
        user = request.user
        serializer = UserSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=True, methods=["post"], permission_classes=[IsAuthenticated])
    def avaliar(self, request, pk=None):
        """Permite que um usuário avalie outro usuário."""
        avaliado = self.get_object()
        avaliado_por = request.user

        if avaliado == avaliado_por:
            return Response(
                {"detail": "Você não pode se auto-avaliar."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        data = request.data.copy()
        data["avaliador"] = avaliado_por.id
        data["avaliado"] = avaliado.id

        serializer = AvaliacaoSerializer(data=data)
        if serializer.is_valid():
            avaliacao = serializer.save()
            # Chamar o método para atualizar o rating do usuário avaliado
            avaliado.atualizar_rating(avaliacao.nota)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=["get"], permission_classes=[IsAuthenticated])
    def avaliacoes(self, request, pk=None):
        """Retorna todas as avaliações recebidas por um usuário."""
        user = self.get_object()
        avaliacoes = Avaliacao.objects.filter(avaliado=user)
        serializer = AvaliacaoSerializer(avaliacoes, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def get_serializer_class(self):
        if self.action == 'list':
            return UserListSerializer
        elif self.action == 'retrieve':
            return UserDetailSerializer
        return UserSerializer
