from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from django.db import models
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView

from core.models import User, Projeto, UserProjeto, Avaliacao
from core.serializers import UserSerializer, UserDetailSerializer, UserListSerializer, UserUpdateSerializer

class UserViewSet(ModelViewSet):
    queryset = User.objects.all().order_by("id")
    serializer_class = UserSerializer

    @action(detail=False, methods=["get"], permission_classes=[IsAuthenticated])
    def me(self, request):
        """Retorna o usuário autenticado"""
        user = request.user
        serializer = UserSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    @action(detail=False, methods=['patch'], permission_classes=[IsAuthenticated])
    def update_me(self, request):
        """Atualiza as informações do usuário autenticado"""
        user = request.user
        serializer = UserUpdateSerializer(user, data=request.data, partial=True)

        if serializer.is_valid():
            if 'foto' in request.FILES:
                user.foto = request.FILES['foto']
            
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=False, methods=["get"], permission_classes=[AllowAny])
    def empresas(self, request):
        """Retorna todos os usuários que são empresas"""
        empresas = User.objects.filter(is_empresa=True)
        serializer = UserListSerializer(empresas, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=False, methods=["get"], permission_classes=[AllowAny])
    def freelancers(self, request):
        """Retorna todos os usuários que são freelancers"""
        freelancers = User.objects.filter(is_empresa=False)
        serializer = UserListSerializer(freelancers, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=True, methods=["post"], permission_classes=[IsAuthenticated])
    def accept_vacancy(self, request, pk=None):
        """Permite que o usuário se candidate a uma vaga especificada pelo id"""
        job = get_object_or_404(Projeto, id=pk)

        if job.isClosed:
            return Response(
                {"error": "Essa vaga está fechada para novas candidaturas"},
                status=status.HTTP_400_BAD_REQUEST
            )

        job.check_max_candidates()

        if UserProjeto.objects.filter(projeto=job, freelancer_user=request.user).exists():
            return Response(
                {"error": "Você já se candidatou a esta vaga"},
                status=status.HTTP_400_BAD_REQUEST
            )

        UserProjeto.objects.create(
            projeto=job,
            freelancer_user=request.user,  
            status=UserProjeto.StatusJob.PENDENTE,   
        )

        return Response(
            {"message": "Você se candidatou com sucesso à vaga"},
            status=status.HTTP_200_OK
        )

    def get_serializer_class(self):
        """Retorna o serializer adequado para a ação"""
        if self.action == 'list':
            return UserListSerializer
        elif self.action == 'retrieve':
            return UserSerializer
        return UserSerializer


class UserRatingsView(APIView):
    def get(self, request, user_id):
        try:
            user = User.objects.get(id=user_id)
            # Calcule a média de avaliações
            total_avaliacoes = Avaliacao.objects.filter(avaliado=user).count()
            if total_avaliacoes > 0:
                total_rating = Avaliacao.objects.filter(avaliado=user).aggregate(models.Avg('nota'))['nota__avg']
            else:
                total_rating = 0
            user.rating = total_rating
            user.total_avaliacoes = total_avaliacoes
            user.save()

            serializer = UserSerializer(user)
            return Response(serializer.data, status=status.HTTP_200_OK)

        except User.DoesNotExist:
            return Response({'error': 'Usuário não encontrado'}, status=status.HTTP_404_NOT_FOUND)