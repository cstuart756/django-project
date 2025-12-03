from django.shortcuts import render, get_object_or_404
from .models import Category, Product

# Home page showing all categories
def home(request):
    categories = Category.objects.all()
    return render(request, 'store/home.html', {'categories': categories})

# Product listing by category
def product_list(request, category_slug):
    category = get_object_or_404(Category, slug=category_slug)
    products = category.products.filter(available=True)
    return render(request, 'store/product_list.html', {'category': category, 'products': products})

# Product detail page
def product_detail(request, product_slug):
    product = get_object_or_404(Product, slug=product_slug)
    return render(request, 'store/product_detail.html', {'product': product})

