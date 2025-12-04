from django.shortcuts import redirect, get_object_or_404
from .models import Productfrom django.shortcuts import render, get_object_or_404
from .models import Category, Product
from django.shortcuts import redirect
from .cart import Cart
from .models import Product
import stripe
from django.conf import settings

stripe.api_key = settings.STRIPE_SECRET_KEY

def checkout(request):
    cart = Cart(request)
    if not cart.cart:
        return redirect('store:home')

    if request.method == 'POST':
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            if request.user.is_authenticated:
                order.user = request.user
            order.save()

            # Create Stripe session
            line_items = []
            for item_id, item in cart.cart.items():
                product = get_object_or_404(Product, id=item_id)
                line_items.append({
                    'price_data': {
                        'currency': 'usd',
                        'product_data': {'name': product.name},
                        'unit_amount': int(product.price * 100),  # cents
                    },
                    'quantity': item['quantity'],
                })

            session = stripe.checkout.Session.create(
                payment_method_types=['card'],
                line_items=line_items,
                mode='payment',
                success_url=request.build_absolute_uri('/checkout/success/'),
                cancel_url=request.build_absolute_uri('/cart/'),
            )
            return redirect(session.url, code=303)
    else:
        form = OrderCreateForm()

    return render(request, 'store/checkout.html', {'cart': cart, 'form': form, 'STRIPE_PUBLIC_KEY': settings.STRIPE_PUBLIC_KEY})
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

def checkout(request):
    cart = Cart(request)
    if not cart.cart:
        return redirect('store:home')

    if request.method == 'POST':
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            if request.user.is_authenticated:
                order.user = request.user
            order.paid = True  # For now, mark as paid
            order.save()
            cart.clear()
            return render(request, 'store/checkout_success.html', {'order': order})
    else:
        form = OrderCreateForm()
def checkout_success(request):
    cart = Cart(request)
    cart.clear()
    return render(request, 'store/checkout_success.html')
    return render(request, 'store/checkout.html', {'cart': cart, 'form': form})
from django.contrib.auth.decorators import login_required

@login_required
def profile(request):
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'store/profile.html', {'orders': orders})
from django.shortcuts import get_object_or_404

@login_required
def order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    items = order.orderitem_set.all()  # Get all items for this order
    return render(request, 'store/order_detail.html', {'order': order, 'items': items})
def cart_detail(request):
    cart = Cart(request)
    products = []
    total = 0
    for item_id, item in cart.cart.items():
        product = get_object_or_404(Product, id=item_id)
        quantity = item['quantity']
        price = float(item['price'])
        subtotal = quantity * price
        total += subtotal
        products.append({
            'product': product,
            'quantity': quantity,
            'price': price,
            'subtotal': subtotal
        })
    return render(request, 'store/cart_detail.html', {'cart_items': products, 'total': total})

def cart_update(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart = Cart(request)
    if request.method == 'POST':
        action = request.POST.get('action')
        quantity = int(request.POST.get('quantity', 1))
        if action == 'update':
            cart.add(product, quantity=quantity, override_quantity=True)
        elif action == 'remove':
            cart.remove(product)
    return redirect('store:cart_detail')