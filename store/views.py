from django.shortcuts import render, get_object_or_404
from .models import Category, Product
from django.shortcuts import redirect
from .cart import Cart
from .models import Product
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

# Add a product to the cart
def add_to_cart(request, product_id):
    cart = Cart(request)
    product = Product.objects.get(id=product_id)
    cart.add(product=product)
    return redirect('store:cart_detail')

# Remove a product from the cart
def remove_from_cart(request, product_id):
    cart = Cart(request)
    product = Product.objects.get(id=product_id)
    cart.remove(product)
    return redirect('store:cart_detail')

# Display the cart
def cart_detail(request):
    cart = Cart(request)
    return render(request, 'store/cart_detail.html', {'cart': cart})

from django.db.models import Q

def home(request):
    categories = Category.objects.all()
    products = Product.objects.all()

    # Search query
    query = request.GET.get('q')
    if query:
        products = products.filter(Q(name__icontains=query) | Q(description__icontains=query))

    # Category filter
    category_slug = request.GET.get('category')
    if category_slug:
        products = products.filter(category__slug=category_slug)

    context = {
        'categories': categories,
        'products': products,
        'selected_category': category_slug,
        'query': query
    }
    return render(request, 'store/home.html', context)
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import UserRegisterForm

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your account has been created! You can now log in.')
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'store/register.html', {'form': form})

