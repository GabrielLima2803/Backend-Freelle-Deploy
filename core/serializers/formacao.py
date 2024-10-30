from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from core.models import Formacao

class FormacaoSerializer(ModelSerializer):
    class Meta:
        model = Formacao
        fields = "__all__"
