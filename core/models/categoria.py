from django.db import models

class Categoria(models.Model):
    nome = models.CharField(max_length=100, null=False, unique=True)
    icon = models.CharField(max_length=100, null=False, blank=True)

    def __str__(self):
        return f"Categoria - {self.nome}"
    
    class Meta:
        verbose_name = "Categoria"
        verbose_name_plural = "Categorias"