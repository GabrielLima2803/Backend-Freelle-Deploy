from django.db import models
from .user import User
from .projeto import Projeto
from django.utils import timezone

class UserProjeto(models.Model):
    class StatusJob(models.IntegerChoices):
        PENDENTE = 1, "Pendente"
        REJEITADO = 2, "Rejeitado"
        SELECIONADO = 3, "Selecionado"
        NÃO_SELECIONADO = 4, "Não selecionado"
    empresa_user = models.ForeignKey(User, related_name="empresa_projects", on_delete=models.CASCADE, blank=True, null=True)
    freelancer_user = models.ForeignKey(User, related_name="freelancer_projects", on_delete=models.CASCADE, blank=True, null=True)
    application_date = models.DateTimeField(default=timezone.now)
    is_selected = models.BooleanField(default=False)
    status = models.IntegerField(choices=StatusJob.choices, default=StatusJob.PENDENTE)
    projeto = models.ForeignKey(Projeto, related_name="candidatos", on_delete=models.CASCADE)

    class Meta:
        verbose_name = "User Projeto"
        verbose_name_plural = "User Projetos"
        unique_together = ["empresa_user", "freelancer_user", "projeto"]
    def __str__(self):
        user_name = getattr(self.empresa_user, 'email', "Sem usuário")
        projeto_name = getattr(self.projeto, 'titulo', "Sem projeto")
        return f"UserProjeto - Client: {user_name} Projeto: {projeto_name}"
