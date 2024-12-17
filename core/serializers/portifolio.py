from core.models import Portifolio
from rest_framework.serializers import ModelSerializer, SlugRelatedField
from uploader.models import Image
from uploader.serializers import ImageSerializer

class PortifolioSerializer(ModelSerializer):
    image_attachment_key = SlugRelatedField(
        source="image",
        queryset=Image.objects.all(),
        slug_field="attachment_key",
        required=False,
        write_only=True,
    )
    image = ImageSerializer(required=False, read_only=True)
    class Meta:
        model = Portifolio
        fields = "__all__"
