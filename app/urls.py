from django.contrib import admin
from django.urls import include, path

from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularRedocView,
    SpectacularSwaggerView,
)
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from core.views import UserViewSet, CategoriaViewSet, FavoritoViewSet, ProjetoViewSet, UserProjetoViewSet, NacionalidadeViewSet, FormacaoViewSet

from core.auth import LoginUser, RegisterUser, ForgotPasswordUser, ResetPasswordUser

router = DefaultRouter()

router.register(r"usuarios", UserViewSet, basename="usuarios")
router.register(r"categorias", CategoriaViewSet, basename="categorias")
router.register(r"favoritos", FavoritoViewSet, basename="favoritos")
router.register(r"projetos", ProjetoViewSet, basename="projetos")
router.register(r"user-projetos", UserProjetoViewSet, basename="user-projetos")
router.register(r"nacionalidades", NacionalidadeViewSet, basename="nacionalidades")
router.register(r"formacao", FormacaoViewSet, basename="formacao")

urlpatterns = [
    path("admin/", admin.site.urls),
    # OpenAPI 3
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    path(
        "api/swagger/",
        SpectacularSwaggerView.as_view(url_name="schema"),
        name="swagger-ui",
    ),
    path(
        "api/redoc/",
        SpectacularRedocView.as_view(url_name="schema"),
        name="redoc",
    ),
    # Simple JWT
    path("token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    # API
    path("api/", include(router.urls)),
    path("api/register/", RegisterUser, name="register"),
    path("api/login/", LoginUser, name="login"),
    path("api/forgot-password/", ForgotPasswordUser, name="forgot-password"),
    path("api/reset-password/", ResetPasswordUser, name="reset-password")
]
