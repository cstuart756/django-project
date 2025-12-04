from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from .models import Product
from .forms import ProductSearchForm, ReviewForm

def product_list(request):
    products = Product.objects.all()
    form = ProductSearchForm(request.GET)

    if form.is_valid():
        if form.cleaned_data['query']:
            products = products.filter(name__icontains=form.cleaned_data['query'])
        if form.cleaned_data['category']:
            products = products.filter(category=form.cleaned_data['category'])
        if form.cleaned_data['min_price']:
            products = products.filter(price__gte=form.cleaned_data['min_price'])
        if form.cleaned_data['max_price']:
            products = products.filter(price__lte=form.cleaned_data['max_price'])

    paginator = Paginator(products, 6)
    page = request.GET.get('page')
    products = paginator.get_page(page)

    return render(request, 'store/product_list.html', {
        'products': products,
        'form': form
    })


def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug)

    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.product = product
            review.user = request.user
            review.save()
            return redirect('product_detail', slug=slug)
    else:
        form = ReviewForm()

    return render(request, 'store/product_detail.html', {
        'product': product,
        'form': form
    })
