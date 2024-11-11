from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from core.models import Nacionalidade

class NacionalidadeSerializer(ModelSerializer):
    class Meta:
        model = Nacionalidade
        fields = "__all__"
