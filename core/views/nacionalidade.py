from rest_framework.viewsets import ModelViewSet
from rest_framework import filters
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from django_filters.rest_framework import DjangoFilterBackend

from core.models import Nacionalidade
from core.serializers import NacionalidadeSerializer

class NacionalidadeViewSet(ModelViewSet):
    queryset = Nacionalidade.objects.all().order_by("id")
    serializer_class = NacionalidadeSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['nome'] 
    search_fields = ['nome']  
    ordering_fields = ['id', 'nome']