from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from .projeto import ProjetoSerializer
from .user import UserSerializer

from core.models import UserProjeto

class UserProjetoSerializer(ModelSerializer):
    fk_client_user = UserSerializer()
    fk_freelancer_user = UserSerializer()
    projeto = ProjetoSerializer()
    class Meta:
        model = UserProjeto
        fields = "__all__"

class UserProjetoDetailSerializer(ModelSerializer):
        fk_client_user = UserSerializer()
        fk_freelancer_user = UserSerializer()
        projeto = ProjetoSerializer()

        class Meta:
             model = UserProjeto
             fields = "__all__"
             depth = 1

class ListUserProjetoSerializer(ModelSerializer):
    fk_client_user = UserSerializer()
    fk_freelancer_user = UserSerializer()
    projeto_status = serializers.CharField(source='projeto.status', read_only=True)
    projeto = ProjetoSerializer()

    class Meta:
        model = UserProjeto
        fields = ['id', 'fk_client_user', 'fk_freelancer_user', 'projeto', 'projeto_status']

