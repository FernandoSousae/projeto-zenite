from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework import permissions
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets, status, serializers


from .permissions import IsInGroup
from .models import NotaFiscal, Recebimento, ItemRecebido, Material, Defeito, InspecaoQualidade, ItemInspecionadoDefeito, PlanoCompra, Fornecedor
from .serializers import NotaFiscalSerializer, RecebimentoSerializer, UserSerializer, DefeitoSerializer, InspecaoQualidadeSerializer, RegistrarDefeitoSerializer, PlanoCompraSerializer, FornecedorSerializer

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
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        """Salva o recebimento associando o usuário logado como o conferente."""
        serializer.save(conferente=self.request.user)


    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def iniciar_inspecao(self, request, pk=None):
        # ... (o método iniciar_inspecao continua aqui, sem alterações) ...
        recebimento = self.get_object()
        if hasattr(recebimento, 'inspecao'):
            return Response(
                {'error': 'Este recebimento já possui uma inspeção associada.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        nova_inspecao = InspecaoQualidade.objects.create(
            recebimento=recebimento,
            revisor=request.user,
            status='PENDENTE'
        )
        serializer = InspecaoQualidadeSerializer(nova_inspecao)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

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