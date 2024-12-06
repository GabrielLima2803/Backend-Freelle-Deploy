from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)
from django.db import models
from datetime import datetime
from uploader.models import Image
from .favorito import Favorito
from .formacao import Formacao
from .nacionalidade import Nacionalidade
import uuid


def generate_unique_passage_id():
    return str(uuid.uuid4())


class UserManager(BaseUserManager):
    """Manager for users."""
    
    use_in_migrations = True

    def create_user(self, email, password=None, **extra_fields):
        """Create, save and return a new user."""
        if not email:
            raise ValueError("Users must have an email address.")

        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password, username=None, **extra_fields):
        """Create, save and return a new superuser."""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get('is_superuser') is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self.create_user(email, password, username=username, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    """User model in the system."""
    username = models.CharField(max_length=255, unique=True, null=True, blank=True)
    name = models.CharField(max_length=255)
    biografia = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    linguagem_principal = models.CharField(max_length=255, null=True, blank=True)
    especializacao = models.CharField(max_length=255, null=True, blank=True)
    # foto = models.ImageField(upload_to='profile_pics/', null=True, blank=True) Resolver erro
    instagram = models.CharField(max_length=255, unique=True, null=True, blank=True)
    linkedin = models.CharField(max_length=255, unique=True, null=True, blank=True)
    isPro = models.BooleanField(default=False)
    passage_id = models.CharField(max_length=255, unique=True, default=generate_unique_passage_id)
    email = models.EmailField(max_length=255, unique=True)
    is_active = models.BooleanField(default=True)
    # expert
    total_pedidos = models.FloatField(default=0)
    
    is_staff = models.BooleanField(default=False)
    reset_code = models.CharField(max_length=6, null=True, blank=True)
    rating = models.FloatField(default=0.0, verbose_name="Média de Avaliações")
    total_avaliacoes = models.PositiveIntegerField(default=0, verbose_name="Total de Avaliações")
    nacionalidade = models.ForeignKey(Nacionalidade, related_name="users", on_delete=models.PROTECT, null=True, blank=True)
    formacao = models.ForeignKey(Formacao, related_name="users", on_delete=models.PROTECT, null=True, blank=True)
    favorito = models.ForeignKey(Favorito, related_name="users", on_delete=models.PROTECT, null=True, blank=True)
    cnpj = models.CharField(max_length=18, unique=True, null=True, blank=True)  
    descricao = models.TextField(null=True, blank=True)  
    is_empresa = models.BooleanField(default=False) 

    objects = UserManager()

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ["email"]
    EMAIL_FIELD = "email"

    class Meta:
        """Meta options for the model."""
        verbose_name = "Usuário"
        verbose_name_plural = "Usuários"

    def __str__(self):
        return self.username or self.email

    def atualizar_rating(self, nova_avaliacao):
        """Atualiza a média de avaliações."""
        total_avaliacoes = self.total_avaliacoes + 1
        nova_media = (self.rating * self.total_avaliacoes + nova_avaliacao) / total_avaliacoes
        self.rating = nova_media
        self.total_avaliacoes = total_avaliacoes
        self.save()


class Avaliacao(models.Model):
    """Modelo para avaliações dos usuários."""
    avaliador = models.ForeignKey(User, related_name="avaliacoes_feitas", on_delete=models.CASCADE)
    avaliado = models.ForeignKey(User, related_name="avaliacoes_recebidas", on_delete=models.CASCADE)
    nota = models.PositiveSmallIntegerField(verbose_name="Nota", choices=[(i, f"{i} Estrela(s)") for i in range(1, 6)])
    comentario = models.TextField(null=True, blank=True)
    data_criacao = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Avaliação"
        verbose_name_plural = "Avaliações"
        unique_together = ("avaliador", "avaliado")  

    def __str__(self):
        return f"{self.avaliador} avaliou {self.avaliado} - {self.nota} Estrela(s)"
