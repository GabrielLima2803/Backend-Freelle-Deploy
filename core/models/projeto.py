from django.db import models
from datetime import datetime
from uploader.models import Image
from .categoria import Categoria
from django.utils import timezone
from .user import User
        
class Projeto(models.Model):
    class StatusChoices(models.IntegerChoices):
        CLOSE = 1, 'Fechado'
        PROGESS = 2, 'Em andamento'
        FINISH = 3, 'Finalizado'

    titulo = models.CharField(max_length=80)
    descricao = models.TextField()
    foto = models.ForeignKey(Image, on_delete=models.SET_NULL, null=True, blank=True)
    status = models.IntegerField(choices=StatusChoices.choices, default=StatusChoices.PROGESS)
    preco = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    prazo_entrega = models.DateField()
    proposta_recebida = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    orcamento = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    data_publicada = models.DateField(default=datetime.now)
    categoria = models.ManyToManyField(Categoria, related_name="projetos")
    isExpired = models.BooleanField(default=False)
    isClosed = models.BooleanField(default=False) 
    max_candidates = models.PositiveIntegerField(default=1)
    selected_user = models.ForeignKey(
        User,
        related_name="selected_jobs",
        null=True,
        blank=True,
        on_delete=models.SET_NULL
    )
    

    class Meta:
        verbose_name = "Projeto"
        verbose_name_plural = "Projetos"

    def __str__(self):
        return f"{self.id} - Projeto - {self.titulo}"


    def check_expiration(self):
        if self.prazo_entrega  < timezone.now().date():
            self.isExpired = True
            self.isClosed = True  
            self.save()
        else:
            self.isExpired = False
            self.save()

    def check_max_candidates(self):
        if self.candidatos.count() >= self.max_candidates:
            self.isClosed = True
            self.save()