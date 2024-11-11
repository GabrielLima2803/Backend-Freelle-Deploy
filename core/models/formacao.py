from django.db import models


class Formacao(models.Model):
    NIVEIS_ACADEMICOS = [
        ('fundamental', 'Ensino Fundamental'),
        ('medio', 'Ensino Médio'),
        ('graduacao', 'Graduação'),
        ('pos_graduacao', 'Pós-Graduação'),
        ('mestrado', 'Mestrado'),
        ('doutorado', 'Doutorado'),
    ]

    nivel_academico = models.CharField(
        max_length=50, 
        choices=NIVEIS_ACADEMICOS, 
        verbose_name='Nível Acadêmico'
    )

    escola_academica = models.CharField(
        max_length=255, 
        verbose_name='Instituição de Ensino'
    )
    class Meta:
        verbose_name = "Formação"
        verbose_name_plural = "Formações"

    def __str__(self):
        return f"{self.nivel_academico} - {self.escola_academica}"
