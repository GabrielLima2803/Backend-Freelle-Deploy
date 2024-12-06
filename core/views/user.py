from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from core.models import User
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
    
    @action(detail=False, methods=['patch'])
    def update_me(self, request):
            user = request.user
            serializer = self.get_serializer(user, data=request.data, partial=True)

            if serializer.is_valid():
                if 'foto' in request.data:
                    user.foto = request.data['foto']
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=400)
    
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


    def get_serializer_class(self):
        if self.action == 'list':
            return UserListSerializer
        elif self.action == 'retrieve':
            return UserDetailSerializer
        return UserSerializer

