from rest_framework.viewsets import ModelViewSet
from rest_framework import filters, status
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend, FilterSet, filters as django_filters
from rest_framework.exceptions import ValidationError


from core.models import Projeto, UserProjeto, User, Categoria
from core.serializers import ProjetoSerializer, UserProjetoSerializer

class ProjetoFilterSet(FilterSet):
    categoria_id = django_filters.NumberFilter(field_name='categoria__id', lookup_expr='exact')

    class Meta:
        model = Projeto
        fields = ['categoria_id']

class ProjetoViewSet(ModelViewSet):
    queryset = Projeto.objects.all().order_by("id")
    serializer_class = ProjetoSerializer
    # permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = ProjetoFilterSet
    search_fields = ['titulo', 'descricao']  
    ordering_fields = ['id', 'titulo', 'data_criacao']

    def get_queryset(self):
        """
        Adiciona verificações de expiração e número máximo de candidatos,
        mas evita loops desnecessários.
        """
        queryset = super().get_queryset()
        for projeto in queryset:
            projeto.check_expiration()
            projeto.check_max_candidates()
        return queryset
    

    def get_serializer_class(self):
        return self.serializer_class
    # def destroy(self, request, *args, **kwargs):
    #     """
    #     Exclui um projeto, se possível.
    #     """
    #     projeto = self.get_object()  # Pega o projeto com base no ID da URL
    #     try:
    #         projeto.delete()  # Exclui o projeto
    #         return Response(
    #             {"message": "Projeto excluído com sucesso."},
    #             status=status.HTTP_204_NO_CONTENT
    #         )
    #     except Exception as e:
    #         return Response(
    #             {"error": f"Ocorreu um erro ao tentar excluir o projeto: {str(e)}"},
    #             status=status.HTTP_400_BAD_REQUEST
    #         )
    def create(self, request, *args, **kwargs):
        """
        Cria um projeto com os dados do formulário e um campo de imagem (arquivo).
        Também cria automaticamente um UserProjeto associado ao usuário autenticado.
        """
        image_file = request.FILES.get("image_project")
        categoria_id = request.data.get("categoria")

        if not image_file:
            return Response(
                {"error": "A imagem (foto) é obrigatória."},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            from uploader.models import Image
            imagem = Image.objects.create(file=image_file)

            categoria = Categoria.objects.get(pk=categoria_id)

            projeto = Projeto.objects.create(
                foto=imagem,
                titulo=request.data.get("titulo"),
                descricao=request.data.get("descricao"),
                prazo_entrega=request.data.get("prazo_entrega") or None,
                max_candidates=request.data.get("max_candidates") or None,
                orcamento=request.data.get("orcamento") or None
            )
            projeto.categoria.set([categoria])

            UserProjeto.objects.create(
                empresa_user=request.user,
                projeto=projeto,
                status=UserProjeto.StatusJob.PENDENTE
            )

            return Response(
                {"id": projeto.id, "message": "Projeto criado com sucesso!"},
                status=status.HTTP_201_CREATED
            )

        except Exception as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )

    @action(detail=True, methods=["post"])
    def select_candidate(self, request, pk=None):
        """
        Permite que a empresa selecione um candidato para uma vaga e remova outros candidatos da vaga.
        """
        projeto = get_object_or_404(Projeto, pk=pk)  # Busca o projeto pelo ID

        application_id = request.data.get("application_id")
        if not application_id:
            return Response(
                {"error": "O ID da aplicação é obrigatório."},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            application = UserProjeto.objects.get(id=application_id, projeto=projeto)
        except UserProjeto.DoesNotExist:
            return Response(
                {"error": "Aplicação não encontrada para esse projeto."},
                status=status.HTTP_404_NOT_FOUND
            )

        # Verificando se o candidato já foi selecionado
        if application.is_selected:
            return Response(
                {"error": "Este candidato já foi selecionado."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Atualizando os outros candidatos para não selecionados
        projeto.candidatos.exclude(id=application_id).update(
            is_selected=False, status=UserProjeto.StatusJob.REJEITADO
        )

        # Selecionando o candidato atual
        application.is_selected = True
        application.status = UserProjeto.StatusJob.SELECIONADO
        application.save()

        # Atualizando o projeto com o candidato selecionado
        projeto.selected_user = application.user  # Aqui estamos acessando o campo `user` do candidato
        projeto.save()

        # Fechando o projeto se o número máximo de candidatos foi atingido
        if projeto.max_candidates == projeto.candidatos.filter(is_selected=True).count():
            projeto.isClosed = True
            projeto.save()

        return Response(
            {"message": "Candidato selecionado com sucesso e outros candidatos removidos."},
            status=status.HTTP_200_OK
        )

    @action(detail=False, methods=['get'], url_path='current-projetos', url_name='current_projetos', permission_classes=[IsAuthenticated])
    def current_projetos(self, request):
        """
        Retorna uma lista com os projetos em andamento do usuário logado.
        """
        user = request.user

        if UserProjeto.objects.filter(empresa_user=user).exists():
            projetos_ids = UserProjeto.objects.filter(empresa_user=user).values_list('projeto_id', flat=True)
        elif UserProjeto.objects.filter(freelancer_user=user).exists():
            projetos_ids = UserProjeto.objects.filter(freelancer_user=user).values_list('projeto_id', flat=True)
        else:
             return Response({"detail": "Nenhum projeto encontrado para o usuário autenticado."})

        queryset = Projeto.objects.filter(id__in=projetos_ids)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


    @action(detail=False, methods=['get'], url_path='candidatos-da-empresa', url_name='candidatos_da_empresa', permission_classes=[IsAuthenticated])
    def candidatos_da_empresa(self, request):
        """
        Retorna os candidatos de todos os projetos de uma empresa.
        """
        user = request.user
        
        projetos_empresa = Projeto.objects.filter(candidatos__empresa_user=user).distinct()

        candidatos = []
        for projeto in projetos_empresa:
            candidatos_projeto = projeto.candidatos.filter(projeto=projeto)
            candidatos.append({
                'id_projeto': projeto.id,
                'projeto': projeto.titulo,
                'candidatos': UserProjetoSerializer(candidatos_projeto, many=True).data
            })

        return Response(candidatos)
    
    @action(detail=False, methods=['get'], url_path='meus-projetos-candidatados', url_name='meus_projetos_candidatados', permission_classes=[IsAuthenticated])
    def meus_projetos_candidatados(self, request):
        """
        Retorna os projetos nos quais o usuário logado se candidatou como freelancer.
        """
        user = request.user

        # Filtra os projetos onde o usuário é um freelancer e fez uma candidatura
        projetos_ids = UserProjeto.objects.filter(freelancer_user=user).values_list('projeto_id', flat=True)
        if not projetos_ids:
            return Response({"detail": "Você não se candidatou a nenhum projeto."}, status=status.HTTP_404_NOT_FOUND)

        queryset = Projeto.objects.filter(id__in=projetos_ids)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)