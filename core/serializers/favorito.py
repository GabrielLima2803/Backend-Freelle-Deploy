from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from core.models import Favorito

class FavoritoSerializer(ModelSerializer):
    class Meta:
        model = Favorito
        fields = "__all__"

    # def validate_nome(self, value):
    #     if len(value) < 3:
    #         raise serializers.ValidationError("O nome deve ter pelo menos 3 caracteres.")
    #     return value