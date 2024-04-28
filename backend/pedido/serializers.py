from rest_framework import serializers

from .models import Pedido, ItemPedido

from produto.serializers import ProdutoSerializer


class MeuItemPedidoSerializer(serializers.ModelSerializer):
    produto = ProdutoSerializer()

    class Meta:
        model = ItemPedido
        fields = (
            "preco",
            "produto",
            "quantidade",
        )


class MeuPedidorSerializer(serializers.ModelSerializer):
    items = MeuItemPedidoSerializer(many=True)

    class Meta:
        model = Pedido
        fields = (
            "id",
            "primeiro_nome",
            "ultimo_nome",
            "email",
            "endereco",
            "cep",
            "lugar",
            "fone",
            "stripe_token",
            "items",
            "total_pago",
        )


class ItemPedidoSerializer(serializers.ModelSerializer):
    class Meta:
        model = ItemPedido
        fields = (
            "preco",
            "produto",
            "quantidade",
        )


class PedidoSerializer(serializers.ModelSerializer):
    items = ItemPedidoSerializer(many=True)

    class Meta:
        model = Pedido
        fields = (
            "id",
            "primeiro_nome",
            "ultimo_nome",
            "email",
            "endereco",
            "cep",
            "lugar",
            "fone",
            "stripe_token",
            "items",
        )

    def create(self, validated_data):
        items_data = validated_data.pop("items")
        pedido = Pedido.objects.create(**validated_data)

        for item_data in items_data:
            ItemPedido.objects.create(pedido=pedido, **item_data)

        return pedido
