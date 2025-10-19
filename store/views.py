from django.http import Http404
from django.shortcuts import get_object_or_404, render

from .models import Category, Product


def product_all(request):
    products = Product.products.all()
    return render(request, 'store/home.html', {'products': products})


def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug, in_stock=True)
    return render(
        request,
        'store/products/single.html',
        {
            'product': product,
            'quantity_range': range(1, 11),
        },
    )

def category_list(request, category_path):
    slugs = [slug for slug in category_path.strip('/').split('/') if slug]
    if not slugs:
        raise Http404()

    category = get_object_or_404(Category, slug=slugs[-1])
    if category.get_full_slug() != '/'.join(slugs):
        raise Http404()

    descendants = category.get_descendants()
    products = Product.products.filter(category__in=[category, *descendants])
    breadcrumbs = [*category.get_ancestors(), category]
    context = {
        'category': category,
        'products': products,
        'breadcrumbs': breadcrumbs,
    }
    return render(request, 'store/products/category.html', context)
