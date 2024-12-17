from rest_framework import serializers
from rest_framework.serializers import ModelSerializer, SlugRelatedField
from core.models import Projeto
from uploader.models import Image
from uploader.serializers import ImageSerializer
from core.serializers.projetoUser import UserProjetoSerializer


class ProjetoSerializer(ModelSerializer):
    image_project_attachment_key = SlugRelatedField(
        source="foto",
        queryset=Image.objects.all(),
        slug_field="attachment_key", 
        required=False,
        write_only=True,
    )
    foto = ImageSerializer(required=False, read_only=True) 
    preco = serializers.DecimalField(
        max_digits=10, decimal_places=2, default=0, required=False, allow_null=True
    )
    candidatos = UserProjetoSerializer(many=True, read_only=True)  
    remaining_spots = serializers.SerializerMethodField()

    def get_remaining_spots(self, instance):
        if instance.isClosed:
            return "Vagas acabaram"
        
        if instance.candidatos.filter(is_selected=True).exists():
            return "Vaga já foi selecionada"
        
        return max(0, instance.max_candidates - instance.candidatos.count())

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


# class ProjetoDetailSerializer(ModelSerializer):
#     class Meta:
#         model = Projeto
#         fields = "__all__"
#         depth = 1


# class ProjetoListSerializer(ModelSerializer):
#     class Meta:
#         model = Projeto
#         fields = ['id', 'titulo', 'descricao', 'status', 'categoria']
#         depth = 1
