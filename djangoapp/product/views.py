from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views import View
from django.contrib import messages
# from django.http import HttpResponse
from django.urls import reverse
from product.models import Product, Variation

from pprint import pprint


# Create your views here.


class ProductList(ListView):
    model = Product
    template_name = 'product/pages/index.html'
    context_object_name = 'products'
    ordering = '-pk',
    paginate_by = 9


class ProducDetails(DetailView):
    model = Product
    template_name = 'product/pages/product.html'
    context_object_name = 'products'
    slug_field = 'slug'


class AddToCart(View):
    # def get -> get no valor fornecido por input
    def get(self, *args, **kwargs):
        # método para voltar para a url anterior
        http_referer = self.request.META.get(
            'HTTP_REFERER', reverse('product_app:index',)
        )

        # salvando valor fornecido por input no arquivo html,
        # no caso eu estou dando um get no valor do name "vid"
        variation_id = self.request.GET.get('vid')

        # se não tiver algum valor, ou seja, se não tiver o produto,
        # eu retorno uma mensagem de erro
        if not variation_id:
            messages.error(
                self.request,
                "Produto não existe"
            )
            return redirect(http_referer)

        # pego as informações do meu obj passando a classe e o id
        variation = get_object_or_404(Variation, id=variation_id)
        variation_stock = variation.stock
        product = variation.product
        product_id = product.pk
        product_name = product.name
        variation_name = variation.name
        price_unit = variation.price
        price_unit_promotional = variation.price_promotional
        slug = product.slug
        image = product.image.name

        if variation_stock < 1:
            messages.error(
                self.request,
                'Item fora de estoque'
            )
            return redirect(http_referer)

        # trabalhando com sessões
        # se não tiver uma sessão criada, eu crio
        if not self.request.session.get('cart'):
            self.request.session['cart'] = {}
            self.request.session.save()

        # instanciando uma sessão numa variável
        cart = self.request.session['cart']

        if variation_id in cart:
            cart_quantity = cart[variation_id]['amount']
            cart_quantity += 1

            if variation_stock <= cart_quantity:
                messages.warning(
                    self.request,
                    f'Quantidade desejada não disponivel, \
                    restam apenas {variation_stock} produtos restantes. \
                    Adicionei esses {variation_stock} produtos disponiveis \
                    no seu carrinho'
                )

                cart_quantity = variation_stock

            cart[variation_id]['amount'] = cart_quantity

            cart[variation_id]['quantitative_price'] = price_unit * \
                cart_quantity

            cart[variation_id]['quantitative_price_promotional'] = (
                price_unit_promotional * cart_quantity
            )

        else:
            cart[variation_id] = {
                'product_id': product_id,
                'product_name': product_name,
                'variation_id': variation_id,
                'variation_name': variation_name,
                'price_unit': price_unit,
                'price_unit_promotional': price_unit_promotional,
                'quantitative_price': price_unit,
                'quantitative_price_promotional': price_unit_promotional,
                'amount': 1,
                'slug': slug,
                'image': image,
            }

        self.request.session.save()
        pprint(cart)
        messages.success(
            self.request,
            f'Itens adicionados com sucesso:  \
            {product_name} - {variation_name} | \
            Quantidade: {cart[variation_id]["amount"]}x'
        )
        return redirect(http_referer)


class RemoveFromCart(View):
    def get(self, *args, **kwargs):
        http_referer = self.request.META.get(
            'HTTP_REFERER', reverse('product_app:index',)
        )

        # salvando valor fornecido por input no arquivo html,
        # no caso eu estou dando um get no valor do name "vid"
        variation_id = self.request.GET.get('vid')

        if not variation_id:
            print('cai no 1')
            return redirect(http_referer)

        if not self.request.session.get('cart'):
            print('cai no 2')
            return redirect(http_referer)

        if variation_id not in self.request.session['cart']:
            print('cai no 3')
            print(self.request.session['cart'])
            print()
            print(variation_id)
            return redirect(http_referer)

        cart = self.request.session['cart'][variation_id]

        messages.success(
            self.request,
            f'Produto {cart['product_name']} removido do carrinho'
        )

        del self.request.session['cart'][variation_id]
        self.request.session.save()
        return redirect(http_referer)


class Cart(ListView):
    model = Product
    template_name = 'product/pages/cart.html'
    ordering = '-pk',
    paginate_by = 9


class Finish(View):
    ...
