from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from .user import UserDetailSerializer
from core.models import UserProjeto

class UserProjetoSerializer(ModelSerializer):
    # user = serializers.SerializerMethodField()
    status = serializers.CharField(source="get_status_display")

    class Meta:
        model = UserProjeto
        fields = ["id", "freelancer_user", "application_date", "status"]
        depth = 1

    # def get_user(self, obj):
    #     # Retorna apenas o freelancer_user
    #     return UserDetailSerializer(obj.freelancer_user).data
    
# class UserProjetoDetailSerializer(ModelSerializer):
#         fk_empresa_user = UserSerializer()
#         fk_freelancer_user = UserSerializer()
#         projeto = ProjetoSerializer()

#         class Meta:
#              model = UserProjeto
#              fields = "__all__"
#              depth = 1

# class ListUserProjetoSerializer(ModelSerializer):
#     fk_empresa_user = UserSerializer()
#     fk_freelancer_user = UserSerializer()
#     projeto_status = serializers.CharField(source='projeto.status', read_only=True)
#     projeto = ProjetoSerializer()

#     class Meta:
#         model = UserProjeto
#         fields = ['id', 'fk_empresa_user', 'fk_freelancer_user', 'projeto', 'projeto_status']

# class ProjetoUserSmallSerializaer(serializers.ModelSerializer):
#      user = UserDetailSerializer(read_only=True)
#      class Meta:
#         model = UserProjeto
#         fields = ["id", "user"]
#         depth = 1