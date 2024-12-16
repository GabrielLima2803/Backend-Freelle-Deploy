from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from .user import UserDetailSerializer
from core.models import UserProjeto

class UserProjetoSerializer(ModelSerializer):
    status = serializers.CharField(source="get_status_display")
    freelancer_user = UserDetailSerializer(read_only=True)
    empresa_nome = serializers.CharField(source="empresa_user.nome", read_only=True)      
    class Meta:
        model = UserProjeto
        fields = ["id", "freelancer_user", "application_date", "status", "empresa_nome"]
        depth = 1


