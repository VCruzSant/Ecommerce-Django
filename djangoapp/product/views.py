from typing import Any
from django.http import HttpRequest
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views import View
from django.contrib import messages
from django.urls import reverse
from product.models import Product, Variation
from django.db.models import Q
from user_profile.models import UserProfile

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
            return redirect(http_referer)

        if not self.request.session.get('cart'):
            return redirect(http_referer)

        if variation_id not in self.request.session['cart']:
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


class PurchaseSummary(View):
    template_name = 'product/pages/purchase_summary.html'

    def get(self, *args, **kwargs):
        perfil = UserProfile.objects.filter(user=self.request.user).exists()

        if not self.request.user.is_authenticated or not perfil:
            return redirect('user_profile:register')

        if not self.request.session['cart']:
            messages.error(
                self.request,
                'Carrinho vazio'
            )
            return redirect('product_app:index')

        context = {
            'user': self.request.user,
            'cart': self.request.session['cart'],
        }

        return render(
            self.request, self.template_name, context)


class Search(ProductList):
    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs)
        self._search_value = ''

    def setup(self, request: HttpRequest, *args: Any, **kwargs: Any) -> None:
        self._search_value = request.GET.get('search', '').strip()
        return super().setup(request, *args, **kwargs)

    def get(self, request: HttpRequest, *args: Any, **kwargs: Any):
        if self._search_value == '':
            return redirect('product_app:index')
        return super().get(request, *args, **kwargs)

    def get_queryset(self):
        return super().get_queryset().filter(
            Q(name__icontains=self._search_value) |
            Q(description_short__icontains=self._search_value) |
            Q(price_marketing__icontains=self._search_value)
        )[:9]

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context.update({
            'search_value': self._search_value,
        })
        return context
