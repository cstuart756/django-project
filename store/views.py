from django.core.paginator import Paginatorfrom django.shortcuts import render, get_object_or_404
from .models import Category, Product
from django.shortcuts import redirect
from .cart import Cart
from .models import Product
# Home page showing all categories
from django.db.models import Qdef home(request):
    categories = Category.objects.all()
    return render(request, 'store/home.html', {'categories': categories})
def search_products(request):
    query = request.GET.get('q', '')
    products = Product.objects.filter(
        Q(name__icontains=query) | Q(description__icontains=query)
    )
    categories = Category.objects.all()
    return render(request, 'store/product_list.html', {
        'products': products,
        'categories': categories,
        'search_query': query
    })
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

ef paginate_products(request, products, per_page=6):
    paginator = Paginator(products, per_page)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return page_obj

def product_list(request, category_slug=None):
    category = None
    products = Product.objects.all()
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)
    categories = Category.objects.all()

    page_obj = paginate_products(request, products)
    return render(request, 'store/product_list.html', {
        'category': category,
        'categories': categories,
        'page_obj': page_obj
    })

def search_products(request):
    query = request.GET.get('q', '')
    products = Product.objects.filter(
        Q(name__icontains=query) | Q(description__icontains=query)
    )
    categories = Category.objects.all()
    page_obj = paginate_products(request, products)
    return render(request, 'store/product_list.html', {
        'products': products,
        'categories': categories,
        'search_query': query,
        'page_obj': page_obj
    })