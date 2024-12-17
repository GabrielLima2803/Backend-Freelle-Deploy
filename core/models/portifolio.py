from django.db import models
from uploader.models import Image
from .categoria import Categoria

class Portifolio(models.Model):
    image = models.ForeignKey(
        Image,
        related_name="+",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        default=None,
    )
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return f"{self.id} - Portifólio"
