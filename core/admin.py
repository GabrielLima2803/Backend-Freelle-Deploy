from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _

from core import models


class UserAdmin(BaseUserAdmin):
    """Define the admin pages for users."""
    
    ordering = ["id"]
    
    # Atualize list_display para incluir todos os campos desejados
    list_display = (
        'username', 'email', 'name', 'biografia', 'linguagem_principal', 'especializacao',
        'instagram', 'linkedin', 'isPro', 'passage_id', 'is_active', 'is_staff', 'is_empresa',
        'total_pedidos', 'area_atuacao', 'rating', 'total_avaliacoes', 'nacionalidade', 'formacao',
        'favorito', 'cnpj', 'descricao', 'telefone', 'created_at'
    )
    
    # Atualize fieldsets para incluir todos os campos desejados
    fieldsets = (
        (None, {"fields": ("email", "password")}),
        (_("Personal Info"), {"fields": (
            "username", "name", "biografia", "linguagem_principal", "especializacao", "foto", 
            "instagram", "linkedin", "isPro", "passage_id", "created_at"
        )}),
        (_("Company Info"), {"fields": (
            "cnpj", "descricao", "telefone", "is_empresa"
        )}),
        (_("Permissions"), {
            "fields": ("is_active", "is_staff", "is_superuser", "groups", "user_permissions")
        }),
        (_("Important dates"), {"fields": ("last_login",)}),
        (_("Related Fields"), {"fields": (
            "portifolio", "nacionalidade", "formacao", "favorito", "total_pedidos", "area_atuacao", 
            "rating", "total_avaliacoes"
        )}),
    )
    
    readonly_fields = ["last_login", "created_at"]
    
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "email", "password1", "password2", "username", "name", "biografia", "linguagem_principal",
                    "especializacao", "foto", "instagram", "linkedin", "isPro", "passage_id", "is_active", 
                    "is_staff", "is_superuser", "portifolio", "nacionalidade", "formacao", "favorito"
                ),
            },
        ),
    )


admin.site.register(models.User, UserAdmin)
admin.site.register(models.Categoria)
admin.site.register(models.Favorito)
admin.site.register(models.Projeto)
admin.site.register(models.UserProjeto)
admin.site.register(models.Nacionalidade)
admin.site.register(models.Formacao)
admin.site.register(models.Portifolio)
