from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)
from django.db import models
from datetime import datetime
from uploader.models import Image
from .comentario import Comentario
from .favorito import Favorito
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
    biografia = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True) 
    nacionalidade = models.ForeignKey(Nacionalidade, related_name="users", on_delete=models.PROTECT, null=True, blank=True)
    linguagem_principal = models.CharField(max_length=255, null=True, blank=True)
    especializacao = models.CharField(max_length=255, null=True, blank=True)
    foto = models.ForeignKey(Image, related_name="+", on_delete=models.SET_NULL, null=True, blank=True, default=None)
    instagram = models.CharField(max_length=255, unique=True, null=True, blank=True)
    linkedin = models.CharField(max_length=255, unique=True, null=True, blank=True)
    isPro = models.BooleanField(default=False)
    passage_id = models.CharField(max_length=255, unique=True, default=generate_unique_passage_id)
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    comentario = models.ForeignKey(Comentario, related_name="users", on_delete=models.PROTECT, null=True, blank=True)
    favorito = models.ForeignKey(Favorito, related_name="users", on_delete=models.PROTECT, null=True, blank=True)
    reset_code = models.CharField(max_length=6, null=True, blank=True)

    objects = UserManager()

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ["email"]
    EMAIL_FIELD = "email"

    class Meta:
        """Meta options for the model."""

        verbose_name = "Usuário"
        verbose_name_plural = "Usuários"
