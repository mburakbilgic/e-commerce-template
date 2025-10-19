from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render

from store.models import Product

from .basket import Basket


def basket_summary(request):
    basket = Basket(request)
    return render(
        request,
        'store/basket/summary.html',
        {
            'basket': basket,
        },
    )


def basket_add(request):
    basket = Basket(request)
    if request.POST.get('action') == 'post':
        product_id = int(request.POST.get('productid'))
        try:
            product_qty = int(request.POST.get('productqty'))
        except (TypeError, ValueError):
            product_qty = 1
        product = get_object_or_404(Product, id=product_id)
        basket.add(product=product, qty=product_qty)

        basketqty = basket.__len__()
        response = JsonResponse({
            'qty': basketqty,
        })

        return response


def basket_delete(request):
    basket = Basket(request)
    if request.POST.get('action') == 'post':
        product_id = int(request.POST.get('productid'))
        basket.delete(product=product_id)

        basketqty = basket.__len__()
        baskettotal = basket.get_total_price()
        response = JsonResponse({
            'qty': basketqty,
            'subtotal': format(baskettotal, '.2f'),
            'removed': True,
        })

        return response


def basket_update(request):
    basket = Basket(request)
    if request.POST.get('action') == 'post':
        product_id = int(request.POST.get('productid'))
        try:
            product_qty = int(request.POST.get('productqty'))
        except (TypeError, ValueError):
            product_qty = 1
        basket.update(product=product_id, qty=product_qty)

        basketqty = basket.__len__()
        baskettotal = basket.get_total_price()
        item = basket.get_item(product_id)
        item_total = item['total_price'] if item else 0
        item_price = item['price'] if item else 0
        item_qty = item['qty'] if item else 0
        response = JsonResponse({
            'qty': basketqty,
            'subtotal': format(baskettotal, '.2f'),
            'item_total': format(item_total, '.2f'),
            'item_price': format(item_price, '.2f'),
            'item_qty': item_qty,
            'removed': item is None,
        })

        return response
