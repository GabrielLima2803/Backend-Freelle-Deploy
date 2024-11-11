from rest_framework import serializers
from rest_framework.serializers import ModelSerializer, SlugRelatedField
from core.models import User
from uploader.models import Image
from uploader.serializers import ImageSerializer
from .avalicao import AvaliacaoSerializer

class UserSerializer(ModelSerializer):
    foto_attachment_key = SlugRelatedField(
        source="foto",
        queryset=Image.objects.all(),
        slug_field="attachment_key",
        required=False,
        write_only=True,
    )
    foto = ImageSerializer(required=False, read_only=True)

    rating = serializers.FloatField(read_only=True)
    total_avaliacoes = serializers.IntegerField(read_only=True)

    avaliacoes_recebidas = AvaliacaoSerializer(many=True, read_only=True)

    class Meta:
        model = User
        fields = "__all__"


class UserDetailSerializer(ModelSerializer):
    avaliacoes_recebidas = AvaliacaoSerializer(many=True, read_only=True)

    class Meta:
        model = User
        fields = "__all__"
        depth = 1


class UserListSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = [
            'id', 'name', 'email', 'username', 'isPro', 
            'especializacao', 'instagram', 'linkedin', 'rating'
        ]

class UserUpdateSerializer(serializers.ModelSerializer):
    foto = serializers.ImageField(required=False)  

    class Meta:
        model = User
        fields = ["name", "email", "nacionalidade", "foto", "especializacao", "instagram", "linkedin", "username", "formacao"]
        extra_kwargs = {
            "name": {"required": False},
            "email": {"required": False},
            "nacionalidade": {"required": False},
        }

    def update(self, instance, validated_data):
        foto = validated_data.get('foto', None)
        if foto:
            instance.foto = foto
        return super().update(instance, validated_data)