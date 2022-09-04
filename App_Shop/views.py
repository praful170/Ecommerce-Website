from django.shortcuts import render

from django.views.generic import ListView,DetailView

from .models import Product
from django.contrib.auth.mixins import LoginRequiredMixin

# Create your views here.
class Home(ListView):
    model = Product
    template_name = 'App_Shop/home.html'

class Product_Details(DetailView):
    model = Product
    template_name = 'App_Shop/product_details.html'
