from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework import permissions
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import status

from .permissions import IsInGroup
from .models import NotaFiscal, Recebimento, ItemRecebido, Material, Defeito, InspecaoQualidade, ItemInspecionadoDefeito
from .serializers import NotaFiscalSerializer, RecebimentoSerializer, UserSerializer, DefeitoSerializer, InspecaoQualidadeSerializer, InspecaoQualidadeSerializer, RegistrarDefeitoSerializer

@api_view(['GET']) # Este decorator diz que esta view só aceita requisições do tipo GET
def conciliar_recebimento(request, recebimento_id):
    """
    Endpoint da API para disparar a conciliação de um recebimento específico.
    """
    try:
        # 1. Busca o recebimento no banco de dados pelo ID fornecido na URL
        recebimento = Recebimento.objects.get(pk=recebimento_id)

        # 2. Executa o método que já criamos e testamos
        resultado_divergencias = recebimento.realizar_conciliacao()

        # 3. Retorna o resultado como uma resposta JSON
        return Response(resultado_divergencias, status=status.HTTP_200_OK)

    except Recebimento.DoesNotExist:
        # Se o ID não for encontrado, retorna um erro 404
        return Response(
            {"error": f"Recebimento com ID {recebimento_id} não encontrado."},
            status=status.HTTP_404_NOT_FOUND
        )
    
# Adicione ao final de core/views.py
from rest_framework import viewsets
from .models import PlanoCompra, Fornecedor
from .serializers import PlanoCompraSerializer, FornecedorSerializer

class PlanoCompraViewSet(viewsets.ModelViewSet):
    """
    ViewSet para visualizar, criar, editar e deletar Planos de Compra.
    """
    queryset = PlanoCompra.objects.all().order_by('-data_emissao')
    serializer_class = PlanoCompraSerializer

class FornecedorViewSet(viewsets.ModelViewSet):
    queryset = Fornecedor.objects.all().order_by('nome_fantasia')
    serializer_class = FornecedorSerializer
    permission_classes = [permissions.IsAuthenticated, IsInGroup('Administrador', 'Analista')]

class CustomLoginView(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)

        # Serializamos os dados do usuário para incluir na resposta
        user_serializer = UserSerializer(user)

        return Response({
            'token': token.key,
            'user': user_serializer.data
        })

class NotaFiscalViewSet(viewsets.ModelViewSet):
    queryset = NotaFiscal.objects.all().order_by('-data_emissao')
    serializer_class = NotaFiscalSerializer
    permission_classes = [permissions.IsAuthenticated, IsInGroup('Administrador', 'Analista')]

class RecebimentoViewSet(viewsets.ModelViewSet):
    queryset = Recebimento.objects.all().order_by('-data_recebimento')
    serializer_class = RecebimentoSerializer
    # Vamos permitir que Conferentes e papéis superiores acessem
    permission_classes = [permissions.IsAuthenticated, IsInGroup('Administrador', 'Analista', 'Revisor', 'Conferente')]

    def perform_create(self, serializer):
        """Salva o recebimento associando o usuário logado como o conferente."""
        serializer.save(conferente=self.request.user)

    @action(detail=True, methods=['post'])
    def adicionar_item(self, request, pk=None):
        """Ação para adicionar um item contado a um recebimento existente."""
        recebimento = self.get_object()
        serializer = ItemRecebidoCreateSerializer(data=request.data)

        if serializer.is_valid():
            material_id = serializer.validated_data['material_id']
            quantidade = serializer.validated_data['quantidade_contada']

            try:
                material = Material.objects.get(id=material_id)
                # Cria o novo item e o associa a este recebimento
                ItemRecebido.objects.create(
                    recebimento=recebimento,
                    material=material,
                    quantidade_contada=quantidade
                )
                return Response({'status': 'item adicionado'}, status=status.HTTP_201_CREATED)
            except Material.DoesNotExist:
                return Response({'error': 'Material não encontrado'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class DefeitoViewSet(viewsets.ModelViewSet):
    """ API para visualizar e gerenciar os tipos de defeito. """
    queryset = Defeito.objects.all().order_by('nome')
    serializer_class = DefeitoSerializer
    permission_classes = [permissions.IsAuthenticated, IsInGroup('Administrador')]


class InspecaoQualidadeViewSet(viewsets.ModelViewSet):
    """ API para visualizar e gerenciar as Inspeções de Qualidade. """
    queryset = InspecaoQualidade.objects.all().order_by('-created_at')
    serializer_class = InspecaoQualidadeSerializer
    permission_classes = [permissions.IsAuthenticated, IsInGroup('Administrador', 'Analista', 'Revisor')]

    def perform_create(self, serializer):
        """ Associa o usuário logado como o revisor da inspeção. """
        serializer.save(revisor=self.request.user)

    @action(detail=True, methods=['post'])
    def registrar_defeito(self, request, pk=None):
        inspecao = self.get_object()
        serializer = RegistrarDefeitoSerializer(data=request.data)

        if serializer.is_valid():
            data = serializer.validated_data
            try:
                item_recebido = ItemRecebido.objects.get(id=data['item_recebido_id'], recebimento=inspecao.recebimento)
                defeito = Defeito.objects.get(id=data['defeito_id'])

                ItemInspecionadoDefeito.objects.create(
                    item_recebido=item_recebido,
                    defeito=defeito,
                    quantidade_defeituosa=data['quantidade_defeituosa']
                )
                return Response({'status': 'defeito registrado'}, status=status.HTTP_201_CREATED)
            except (ItemRecebido.DoesNotExist, Defeito.DoesNotExist):
                return Response({'error': 'Item ou Defeito inválido.'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)