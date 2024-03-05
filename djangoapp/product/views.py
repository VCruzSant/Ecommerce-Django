from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views import View
from django.contrib import messages
from django.http import HttpResponse
from django.urls import reverse
from product.models import Product, Variation


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

        # trabalhando com sessões
        # se não tiver uma sessão criada, eu crio
        if not self.request.session.get('cart'):
            self.request.session['cart'] = {}
            self.request.session.save()

        # instanciando uma sessão numa variável
        cart = self.request.session['cart']

        if variation_id in cart:
            ...
        else:
            ...

        return HttpResponse('Adicionar ao carrinho', variation)


class RemoveFromCart(View):
    ...


class Cart(ListView):
    ...


class Finish(View):
    ...
