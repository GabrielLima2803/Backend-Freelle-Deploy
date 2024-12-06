from rest_framework.viewsets import ModelViewSet
from rest_framework import filters
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from django_filters.rest_framework import DjangoFilterBackend, FilterSet, filters as django_filters

from core.models import Projeto
from core.serializers import ProjetoSerializer, ProjetoListSerializer, ProjetoDetailSerializer

class ProjetoFilterSet(FilterSet):
    categoria_id = django_filters.NumberFilter(field_name='categoria__id', lookup_expr='exact') 

    class Meta:
        model = Projeto
        fields = ['categoria_id']  

class ProjetoViewSet(ModelViewSet):
    queryset = Projeto.objects.all().order_by("id")
    serializer_class = ProjetoSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = ProjetoFilterSet  
    search_fields = ['categoria__id']  
    ordering_fields = ['id', 'titulo']

    def get_queryset(self):
        queryset = super().get_queryset()
        for projeto in queryset:
            projeto.check_expiration()
            projeto.check_max_candidates()
        return queryset

    def get_serializer_class(self):
        if self.action == 'list':
            return ProjetoSerializer
        elif self.action == 'retrieve':
            return ProjetoSerializer
        return ProjetoSerializer
