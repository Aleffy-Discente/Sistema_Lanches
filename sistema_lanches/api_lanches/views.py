from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Cliente, Produto, Pedido
from .serializers import ClienteSerializer, ProdutoSerializer, PedidoSerializer

def home(request):
    return render(request, 'cliente/index.html')

# Endpoints para Cliente
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
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

@api_view(['GET', 'DELETE'])
def cliente_detalhado(request, id):
    try:
        cliente = Cliente.objects.get(id=id)
    except Cliente.DoesNotExist:
        return Response({'error': 'Cliente não encontrado'}, status=404)

    if request.method == 'GET':
        serializer = ClienteSerializer(cliente)
        return Response(serializer.data)

    elif request.method == 'DELETE':
        cliente.delete()
        return Response({'message': 'Cliente deletado com sucesso'}, status=204)

# Endpoints para Produto
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
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

@api_view(['GET', 'DELETE'])
def produto_detalhado(request, id):
    try:
        produto = Produto.objects.get(id=id)
    except Produto.DoesNotExist:
        return Response({'error': 'Produto não encontrado'}, status=404)

    if request.method == 'GET':
        serializer = ProdutoSerializer(produto)
        return Response(serializer.data)

    elif request.method == 'DELETE':
        produto.delete()
        return Response({'message': 'Produto deletado com sucesso'}, status=204)

# Endpoints para Pedido
@api_view(['GET', 'POST'])
def lista_pedidos(request):
    if request.method == 'GET':
        pedidos = Pedido.objects.all()
        serializer = PedidoSerializer(pedidos, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = PedidoSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

@api_view(['GET', 'DELETE'])
def pedido_detalhado(request, id):
    try:
        pedido = Pedido.objects.get(id=id)
    except Pedido.DoesNotExist:
        return Response({'error': 'Pedido não encontrado'}, status=404)

    if request.method == 'GET':
        serializer = PedidoSerializer(pedido)
        return Response(serializer.data)

    elif request.method == 'DELETE':
        pedido.delete()
        return Response({'message': 'Pedido deletado com sucesso'}, status=204)

@api_view(['GET'])
def historico_pedidos(request, id):
    try:
        cliente = Cliente.objects.get(id=id)
    except Cliente.DoesNotExist:
        return Response({'error': 'Cliente não encontrado'}, status=404)

    pedidos = Pedido.objects.filter(cliente=cliente)
    serializer = PedidoSerializer(pedidos, many=True)
    return Response(serializer.data)


