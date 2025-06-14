from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token

from rest_framework import permissions
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Recebimento
from .permissions import IsInGroup
from .serializers import UserSerializer

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
