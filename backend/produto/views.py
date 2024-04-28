from django.db.models import Q
from django.http import Http404

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view

from .models import Produto, Categoria
from .serializers import ProdutoSerializer, CategoriaSerializer

class ListaUltimosProdutos(APIView):
    def get(self, request, format=None):
        produtos = Produto.objects.all()[0:4]
        serializer = ProdutoSerializer(produtos, many=True)
        return Response(serializer.data)

class DetalheProduto(APIView):
    def get_object(self, categoria_slug, produto_slug):
        try:
            return Produto.objects.filter(categoria__slug=categoria_slug).get(slug=produto_slug)
        except Produto.DoesNotExist:
            raise Http404
    
    def get(self, request, categoria_slug, produto_slug, format=None):
        produto = self.get_object(categoria_slug, produto_slug)
        serializer = ProdutoSerializer(produto)
        return Response(serializer.data)

class DetalheCategoria(APIView):
    def get_object(self, categoria_slug):
        try:
            return Categoria.objects.get(slug=categoria_slug)
        except Categoria.DoesNotExist:
            raise Http404
    
    def get(self, request, categoria_slug, format=None):
        categoria = self.get_object(categoria_slug)
        serializer = CategoriaSerializer(categoria)
        return Response(serializer.data)

@api_view(['POST'])
def search(request):
    query = request.data.get('query', '')

    if query:
        produtos = Produto.objects.filter(Q(nome__icontains=query) | Q(descricao__icontains=query))
        serializer = ProdutoSerializer(produtos, many=True)
        return Response(serializer.data)
    else:
        return Response({"products": []})
