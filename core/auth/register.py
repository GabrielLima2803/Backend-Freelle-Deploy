from django.db.models import Q
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework import status

from ..models.user import User

User = get_user_model()

@api_view(["POST"])
@authentication_classes([])
@permission_classes([AllowAny])
def RegisterUser(request):
    username = request.data.get("username")
    email = request.data.get("email")
    password = request.data.get("password")

    if not username or not email or not password:
        return Response(
            {"message": "Dados de usuário inválidos!"}, 
            status=status.HTTP_400_BAD_REQUEST
        )

    if User.objects.filter(username=username).exists():
        return Response(
            {"message": "Usuário já existe"}, 
            status=status.HTTP_400_BAD_REQUEST
        )
    
    if User.objects.filter(email=email).exists():
        return Response(
            {"message": "Email já existe"},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    user = User.objects.create(username=username, email=email)
    user.set_password(password)
    user.save()

    group, created = Group.objects.get_or_create(name="Freelancer")
    user.groups.add(group) 

    response_data = {
        "message": "Usuário criado com sucesso!",
        "id": user.id,
        "username": user.username,
        "email": user.email,
        "group": group.name,
    }
    return Response(response_data, status=status.HTTP_201_CREATED)


@api_view(["POST"])
@authentication_classes([])
@permission_classes([AllowAny])
def RegisterEmpresa(request):
    email = request.data.get("email")
    cnpj = request.data.get("cnpj")
    nome = request.data.get("nome")
    descricao = request.data.get("descricao")
    password = request.data.get("password")

    if not email or not cnpj or not nome or not password:
        return Response(
            {"message": "Todos os campos obrigatórios devem ser preenchidos!"},
            status=status.HTTP_400_BAD_REQUEST
        )

    if User.objects.filter(email=email).exists():
        return Response(
            {"message": "Email já cadastrado!"},
            status=status.HTTP_400_BAD_REQUEST
        )

    if User.objects.filter(cnpj=cnpj).exists():
        return Response(
            {"message": "CNPJ já cadastrado!"},
            status=status.HTTP_400_BAD_REQUEST
        )

    user = User.objects.create(
        email=email,
        username=nome,
        cnpj=cnpj,
        descricao=descricao,  
        is_empresa=True 
    )
    user.set_password(password)
    user.save()

    group, created = Group.objects.get_or_create(name="Empresa")
    user.groups.add(group)

    response_data = {
        "message": "Empresa criada com sucesso!",
        "id": user.id,
        "nome": user.username,
        "email": user.email,
        "cnpj": user.cnpj,
    }
    return Response(response_data, status=status.HTTP_201_CREATED)