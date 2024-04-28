from django.contrib.auth.models import User
from django.db import models

from produto.models import Produto

class Pedido(models.Model):
    user = models.ForeignKey(User, related_name='orders', on_delete=models.CASCADE)
    primeiro_nome = models.CharField(max_length=100)
    ultimo_nome = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    endereco = models.CharField(max_length=100)
    cep = models.CharField(max_length=100)
    lugar = models.CharField(max_length=100)
    fone = models.CharField(max_length=100)
    criado_em = models.DateTimeField(auto_now_add=True)
    total_pago = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)
    stripe_token = models.CharField(max_length=100)

    class Meta:
        ordering = ['-criado_em',]
    
    def __str__(self):
        return self.primeiro_nome

class ItemPedido(models.Model):
    pedido = models.ForeignKey(Pedido, related_name='items', on_delete=models.CASCADE)
    produto = models.ForeignKey(Produto, related_name='items', on_delete=models.CASCADE)
    preco = models.DecimalField(max_digits=8, decimal_places=2)
    quantidade = models.IntegerField(default=1)

    def __str__(self):
        return '%s' % self.id