from django.shortcuts import render
from products.models import ProductCategory,Product
# Create your views here.
def index(request):
    return render(request, 'products/index.html')
def products(request):
    context ={
    'products': Product.objects.all(),
    'categories': ProductCategory.objects.all()

    }
    return render(request, 'products/products.html',context=context)