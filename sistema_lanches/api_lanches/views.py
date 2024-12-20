from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Cliente, Produto, Pedido
from .serializers import ClienteSerializer, ProdutoSerializer, PedidoSerializer


def home(request):
    return render(request, 'cliente/index.html')

def potencia(request):
    return render(request, 'cliente/tales.html')

@api_view(['GET', 'POST'])
def lista_clientes(request):
    if request.method == 'GET':
        clientes = Cliente.objects.all()
        serializer = ClienteSerializer(clientes, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = ClienteSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'DELETE'])
def cliente_detalhado(request, id):
    try:
        cliente = Cliente.objects.get(id=id)
    except Cliente.DoesNotExist:
        return Response({'error': 'Cliente não encontrado'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = ClienteSerializer(cliente)
        return Response(serializer.data)

    elif request.method == 'DELETE':
        if cliente.pedidos.exists():
            return Response({'error': 'Cliente possui pedidos e não pode ser deletado'}, status=status.HTTP_400_BAD_REQUEST)
        cliente.delete()
        return Response({'message': 'Cliente deletado com sucesso'}, status=status.HTTP_204_NO_CONTENT)


@api_view(['GET', 'POST'])
def lista_produtos(request):
    if request.method == 'GET':
        produtos = Produto.objects.all()
        serializer = ProdutoSerializer(produtos, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = ProdutoSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'DELETE'])
def produto_detalhado(request, id):
    try:
        produto = Produto.objects.get(id=id)
    except Produto.DoesNotExist:
        return Response({'error': 'Produto não encontrado'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = ProdutoSerializer(produto)
        return Response(serializer.data)

    elif request.method == 'DELETE':
        produto.delete()
        return Response({'message': 'Produto deletado com sucesso'}, status=status.HTTP_204_NO_CONTENT)


@api_view(['GET', 'POST'])
def lista_pedidos(request):
    if request.method == 'GET':
        pedidos = Pedido.objects.all()
        serializer = PedidoSerializer(pedidos, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        data = request.data
        cliente_id = data.get('cliente')
        produtos_ids = data.get('produtos', [])
        tipo_entrega = data.get('tipo_entrega')
        try:
            cliente = Cliente.objects.get(id=cliente_id)
        except Cliente.DoesNotExist:
            return Response({'error': 'Cliente não encontrado'}, status=404)
        pedido = Pedido(cliente=cliente, tipo_entrega=tipo_entrega)
        pedido.save() 
        total = 0
        for produto_id in produtos_ids:
            try:
                produto = Produto.objects.get(id=produto_id)
                pedido.produtos.add(produto)
                total += produto.preco
            except Produto.DoesNotExist:
                return Response({'error': f'Produto com ID {produto_id} não encontrado'}, status=404)
        pedido.total = total
        pedido.save()
        serializer = PedidoSerializer(pedido)
        return Response(serializer.data, status=201)


@api_view(['GET', 'DELETE'])
def pedido_detalhado(request, id):
    try:
        pedido = Pedido.objects.get(id=id)
    except Pedido.DoesNotExist:
        return Response({'error': 'Pedido não encontrado'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = PedidoSerializer(pedido)
        return Response(serializer.data)

    elif request.method == 'DELETE':
        pedido.delete()
        return Response({'message': 'Pedido deletado com sucesso'}, status=status.HTTP_204_NO_CONTENT)


@api_view(['GET'])
def historico_pedidos(request, id):
    try:
        cliente = Cliente.objects.get(id=id)
    except Cliente.DoesNotExist:
        return Response({'error': 'Cliente não encontrado'}, status=status.HTTP_404_NOT_FOUND)

    pedidos = Pedido.objects.filter(cliente=cliente)
    serializer = PedidoSerializer(pedidos, many=True)
    return Response(serializer.data)


