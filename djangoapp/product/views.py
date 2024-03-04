from django.shortcuts import render
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views import View
from product.models import Product

# Create your views here.


class ProductList(ListView):
    model = Product
    template_name = 'product/pages/index.html'
    context_object_name = 'products'
    ordering = '-pk',
    paginate_by = 2


class ProducDetails(DetailView):
    ...


class AddToCart(View):
    ...


class RemoveFromCart(View):
    ...


class Cart(ListView):
    ...


class Finish(View):
    ...
