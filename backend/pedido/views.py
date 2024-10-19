import stripe

from django.conf import settings
from django.contrib.auth.models import User
from django.http import Http404
from django.shortcuts import render

from rest_framework import status, authentication, permissions
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.views import APIView
from rest_framework.response import Response

from .models import Pedido, ItemPedido
from .serializers import PedidoSerializer, MeuPedidorSerializer

@api_view(['POST'])
@authentication_classes([authentication.TokenAuthentication])
@permission_classes([permissions.IsAuthenticated])
def checkout(request):
    serializer = PedidoSerializer(data=request.data)

    if serializer.is_valid():
        stripe.api_key = settings.STRIPE_SECRET_KEY
        total_pago = sum(item.get('quantidade') * item.get('produto').preco for item in serializer.validated_data['items'])

        try:
            charge = stripe.Charge.create(
                amount=int(total_pago * 100),
                currency='BRL',
                description='Compra da Cheim',
                source=serializer.validated_data['stripe_token']
            )

            serializer.save(user=request.user, total_pago=total_pago)

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ListaPedidos(APIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, format=None):
        orders = Pedido.objects.filter(user=request.user)
        serializer = MeuPedidorSerializer(orders, many=True)
        return Response(serializer.data)
