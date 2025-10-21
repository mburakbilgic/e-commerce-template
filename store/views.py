from django.http import Http404
from django.shortcuts import get_object_or_404, redirect, render

from .models import Category, Product


def product_all(request):
    products = Product.products.all()
    return render(request, 'store/home.html', {'products': products})


def product_detail(request, category_path, slug):
    product = get_object_or_404(Product, slug=slug, in_stock=True)

    expected_path = product.category.get_full_slug()
    normalized_path = '/'.join(segment for segment in category_path.strip('/').split('/') if segment)

    if normalized_path != expected_path:
        return redirect(
            'store:product_detail',
            permanent=True,
            category_path=expected_path,
            slug=product.slug,
        )

    return render(
        request,
        'store/products/single.html',
        {
            'product': product,
        },
    )

def legacy_product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug, in_stock=True)
    return redirect(
        'store:product_detail',
        permanent=True,
        category_path=product.category.get_full_slug(),
        slug=product.slug,
    )


def category_list(request, category_path):
    slugs = [slug for slug in category_path.strip('/').split('/') if slug]
    if not slugs:
        raise Http404()

    category = get_object_or_404(Category, slug=slugs[-1])
    full_slug = category.get_full_slug()
    if full_slug != '/'.join(slugs):
        return redirect('store:category_list', permanent=True, category_path=full_slug)

    descendants = category.get_descendants()
    products = Product.products.filter(category__in=[category, *descendants])
    breadcrumbs = [*category.get_ancestors(), category]
    context = {
        'category': category,
        'products': products,
        'breadcrumbs': breadcrumbs,
    }
    return render(
        request,
        'store/products/category.html',
        context
    )
