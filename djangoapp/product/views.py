from django.shortcuts import render
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views import View

# Create your views here.


class ProductList(ListView):
    ...


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
