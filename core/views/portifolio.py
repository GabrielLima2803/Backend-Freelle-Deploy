from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from uploader.models import Image
from core.models import Portifolio, Categoria
from rest_framework import status
from rest_framework.response import Response
from core.serializers import PortifolioSerializer

class PortifolioViewSet(ModelViewSet):
    queryset = Portifolio.objects.all().order_by("id")
    serializer_class = PortifolioSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def create(self, request):
        image_file = request.FILES.get("image")
        categoria_id = request.data.get("categoria")

        if not image_file or not categoria_id:
            return Response({"error": "Imagem e categoria são obrigatórias."},
                            status=status.HTTP_400_BAD_REQUEST)

        try:
            image = Image.objects.create(file=image_file)
            categoria = Categoria.objects.get(pk=categoria_id)

            portifolio = Portifolio.objects.create(
                image=image,
                categoria=categoria,
            )

            request.user.portifolio.add(portifolio)
            request.user.save()

            return Response(
                {"id": portifolio.id, "message": "Portfólio criado com sucesso!"},
                status=status.HTTP_201_CREATED,
            )
        except Categoria.DoesNotExist:
            return Response({"error": "Categoria não encontrada."},
                            status=status.HTTP_404_NOT_FOUND)