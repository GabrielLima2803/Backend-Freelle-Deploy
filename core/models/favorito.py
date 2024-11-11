from django.db import models
from datetime import datetime


class Favorito(models.Model):
    date_favorite = models.DateField(default=datetime.now)

    def __str__(self):
        return f"Favorito - ${self.id}"
    
    class Meta:
        verbose_name = "Favorito"
        verbose_name_plural = "Favoritos"