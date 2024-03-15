# type: ignore
from django.shortcuts import redirect, reverse
from django.views import View
from django.contrib import messages
from django.views.generic import ListView, DetailView

from utils import total_cart_quantity, total_cart
from product.models import Variation
from order.models import Order, OrderItem
# Create your views here.


class Pay(DetailView):
    template_name = 'order/pages/pay.html'
    model = Order
    pk_url_kwarg = 'pk'
    context_object_name = 'order'


class SaveOrder(View):
    template_name = 'order/pages/pay.html'

    def get(self, *args, **kwargs):
        if not self.request.user.is_authenticated:
            return redirect('user_profile:register')

        if not self.request.session['cart']:
            messages.error(
                self.request,
                'Carrinho vazio'
            )
            return redirect('product_app:index')

        cart = self.request.session.get('cart')
        cart_variation_id = [v for v in cart]
        bd_variations = list(
            Variation.objects.select_related('product')
            .filter(id__in=cart_variation_id)
        )

        for variation in bd_variations:
            vid = str(variation.id)

            stock = variation.stock
            amount_cart = cart[vid]['amount']
            price_unit = cart[vid]['price_unit']
            price_unit_promo = (
                cart[vid]['price_unit_promotional']
            )

            if stock < amount_cart:
                cart[vid]['amount'] = stock
                cart[vid]['quantitative_price'] = price_unit * stock
                cart[vid]['price_unit_promotional'] = (
                    stock * price_unit_promo
                )

                messages.error(
                    self.request,
                    'Estoque insuficiente. '
                    'Reduzimos a quantidade desses produtos. '
                    'Verifique a alteração '
                )

            amount_total = total_cart_quantity.total_cart_quantity(cart)
            value_total = total_cart.total_cart(cart)

            order = Order(
                user=self.request.user,
                total=value_total,
                amount_total=amount_total,

            )
            order.save()

            OrderItem.objects.bulk_create(
                [
                    OrderItem(
                        order=order,
                        product=v['product_name'],
                        product_id=v['product_id'],
                        variation=v['variation_name'],
                        variation_id=v['variation_id'],
                        price=v['price_unit'],
                        price_promotional=v['price_unit_promotional'],
                        amount=v['amount'],
                        image=v['image'],
                    ) for v in cart.values()
                ]
            )

        del self.request.session['cart']

        return redirect(
            'order:pay',
            kwargs={
                'pk': order.pk
            }
        )


class Detail(View):
    ...


class ListOrders(ListView):
    model = Order
    context_object_name = 'orders'
    template_name = 'order/pages/list_orders.html'
    paginate_by = 10
    ordering = ['-id']
