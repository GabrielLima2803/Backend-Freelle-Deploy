from rest_framework.viewsets import ModelViewSet
from rest_framework import filters
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from django_filters.rest_framework import DjangoFilterBackend

from core.models import UserProjeto
from core.serializers import UserProjetoSerializer, ListUserProjetoSerializer, UserProjetoDetailSerializer

class UserProjetoViewSet(ModelViewSet):
    queryset = UserProjeto.objects.all().order_by("id")  
    serializer_class = UserProjetoSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['projeto'] 
    search_fields = ['projeto']  
    ordering_fields = ['id', 'projeto']

    def get_serializer_class(self):
        if self.action == 'list':
            return ListUserProjetoSerializer
        elif self.action == 'retrieve':
            return UserProjetoDetailSerializer
        return UserProjetoSerializer

    # Usuario só vai ver seus projetos
    def get_queryset(self):
        usuario = self.request.user
        if usuario.is_superuser:
            return UserProjeto.objects.all()
        if usuario.groups.filter(name="Administradores"):
            return UserProjeto.objects.all()
        return UserProjeto.objects.filter(usuario=usuario)