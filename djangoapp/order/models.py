from django.db import models
from django.contrib.auth.models import User


# Create your models here.

""" Pedido:
    user - FK User
    total - Float
    status - Choices
        ('A', 'Aprovado'),
        ('C', 'Criado'),
        ('R', 'Reprovado'),
        ('P', 'Pendente'),
        ('E', 'Enviado'),
        ('F', 'Finalizado'),
"""


class Order(models.Model):
    class Meta:
        verbose_name = 'Order'
        verbose_name_plural = 'Orders'

    user = models.ForeignKey(
        User, on_delete=models.CASCADE,
        related_name='order'
    )
    total = models.FloatField()

    amount_total = models.PositiveIntegerField(default=0)

    status = models.CharField(
        default='C', max_length=1,
        choices=(
            ('A', 'approved'),
            ('C', 'Created'),
            ('D', 'Disapproved'),
            ('P', 'Pending'),
            ('S', 'Sent'),
            ('F', 'Finished'),
        )
    )

    def __str__(self) -> str:
        return f'Order number {self.pk}'


"""    ItemPedido:
        pedido - FK pedido
        produto - Char
        produto_id - Int
        variacao - Char
        variacao_id - Int
        preco - Float
        preco_promocional - Float
        quantidade - Int
        imagem - Char
"""


class OrderItem(models.Model):
    class Meta:
        verbose_name = 'Order Item'
        verbose_name_plural = 'Orders Items'

    order = models.ForeignKey(
        Order, on_delete=models.CASCADE,
        related_name='order_item'
    )
    product = models.CharField(max_length=255)
    product_id = models.PositiveIntegerField()
    variation = models.CharField(max_length=255)
    variation_id = models.PositiveIntegerField()
    price = models.FloatField()
    price_promotional = models.FloatField(default=0)
    amount = models.PositiveIntegerField()
    image = models.CharField(max_length=2000)

    def __str__(self) -> str:
        return f'Order item {self.order}'
