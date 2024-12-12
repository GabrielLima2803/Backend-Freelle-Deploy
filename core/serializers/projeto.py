from rest_framework import serializers
from rest_framework.serializers import ModelSerializer, SlugRelatedField
from core.models import Projeto
from uploader.models import Image
from uploader.serializers import ImageSerializer
from core.serializers.projetoUser import UserProjetoSerializer


class ProjetoSerializer(ModelSerializer):
    image_project_attachment_key = SlugRelatedField(
        source="image_project",
        queryset=Image.objects.all(),
        slug_field="attachment_key",
        required=False,
        write_only=True,
    )
    image_project = ImageSerializer(
        required=False,
        read_only=True
    )
    preco = serializers.DecimalField(
        max_digits=10, decimal_places=2, default=0, required=False, allow_null=True
    )
    candidatos = UserProjetoSerializer(many=True, read_only=True)  # Se você tiver um campo 'candidatos' no modelo
    remaining_spots = serializers.SerializerMethodField()

    def get_remaining_spots(self, instance):
        """
        Calcula o número de vagas restantes ou exibe mensagens caso a vaga esteja
        fechada ou já tenha sido selecionada.
        """
        if instance.isClosed:
            return "Vagas acabaram"
        
        # Usar uma consulta eficiente para contar candidatos
        candidatos_count = instance.candidatos.filter(is_selected=True).count()
        
        if candidatos_count >= instance.max_candidates:
            return "Vaga já foi selecionada"
        
        return max(0, instance.max_candidates - candidatos_count)

    def to_representation(self, instance):
        """
        Ajusta a representação do campo 'preco', garantindo que se o valor for None,
        ele será substituído por 'A Combinar'.
        """
        representation = super().to_representation(instance)
        representation['preco'] = representation['preco'] if representation['preco'] is not None else "A Combinar"
        return representation

    class Meta:
        model = Projeto
        fields = "__all__"
        depth = 1


class ProjetoDetailSerializer(ModelSerializer):
    class Meta:
        model = Projeto
        fields = "__all__"
        depth = 1


class ProjetoListSerializer(ModelSerializer):
    class Meta:
        model = Projeto
        fields = ['id', 'titulo', 'descricao', 'status', 'categoria']
        depth = 1
