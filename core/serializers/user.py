from rest_framework import serializers
from rest_framework.serializers import ModelSerializer, SlugRelatedField, SerializerMethodField
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
        depth = 2



class UserDetailSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "email", "is_empresa"]
        depth = 1


class UserListSerializer(ModelSerializer):
    groups = SerializerMethodField()
    class Meta:
        model = User
        fields = [
            'id', 'name', 'email', 'username', 'isPro', 
            'especializacao', 'instagram', 'linkedin', 'rating', "is_empresa", "groups"
        ]
    def get_groups(self, obj):
        return [{"id": group.id, "name": group.name} for group in obj.groups.all()]

class UserUpdateSerializer(serializers.ModelSerializer):
    foto_url = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = [
            "name",
            "email",
            "nacionalidade",
            "foto", 
            "foto_url", 
            "especializacao",
            "instagram",
            "linkedin",
            "username",
            "formacao",
            "biografia",
        ]
        extra_kwargs = {
            "name": {"required": False},
            "email": {"required": False},
            "nacionalidade": {"required": False},
        }

    def get_foto_url(self, obj):
        """Retorna a URL da foto, se existir."""
        if obj.foto and hasattr(obj.foto, "url"):
            return obj.foto.url
        return None

    def update(self, instance, validated_data):
        # Verifica se 'foto' está nos dados validados e atualiza
        foto = validated_data.pop('foto', None)
        if foto:
            instance.foto = foto
        return super().update(instance, validated_data)