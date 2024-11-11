from rest_framework.viewsets import ModelViewSet
from rest_framework import filters
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from django_filters.rest_framework import DjangoFilterBackend

from core.models import Formacao
from core.serializers import FormacaoSerializer

class FormacaoViewSet(ModelViewSet):
    queryset = Formacao.objects.all().order_by("id")
    serializer_class = FormacaoSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['nivel_academico'] 
    search_fields = ['nivel_academico']  
    ordering_fields = ['id', 'nivel_academico']