from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from products.models import ProductCategory, Product, Baskets
from users.models import User
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator


# Create your views here.
def index(request):
    return render(request, 'products/index.html')


# Products URL
def products(request, category_id=None, page_number=1):
    products = Product.objects.filter(category_id=category_id) if category_id else Product.objects.all()
    per_page = 1
    paginator = Paginator(products, per_page)
    products_paginator = paginator.page(page_number)
    context = {
        'products': products_paginator,
        'categories': ProductCategory.objects.all(),
    }
    return render(request, 'products/products.html', context=context)


@login_required
def basket_add(request, product_id):
    product = Product.objects.get(id=product_id)
    baskets = Baskets.objects.filter(user=request.user, product=product)

    if not baskets.exists():
        Baskets.objects.create(user=request.user, product=product, quantity=1)
    else:
        baskets = baskets.first()
        baskets.quantity += 1
        baskets.save()
    return HttpResponseRedirect(request.META['HTTP_REFERER'])


def basket_remove(request, baskets_id):
    basket = Baskets.objects.get(id=baskets_id)
    basket.delete()
    return HttpResponseRedirect(request.META['HTTP_REFERER'])
