from decimal import Decimal, InvalidOperation

from store.models import Product


class Basket():
    """
    A base Basket class, providing some default behaviours that
    can be inherited or overrided, as necessary.
    """

    def __init__(self, request):
        self.session = request.session
        basket = self.session.get('skey')
        if 'skey' not in request.session:
            basket = self.session['skey'] = {}
        self.basket = basket
        self._normalize()

    def _normalize(self):
        """Ensure all basket items share a consistent structure."""
        if not self.basket:
            return

        needs_normalization = {}
        for product_id, item in list(self.basket.items()):
            if isinstance(item, dict) and 'price' in item and 'qty' in item:
                try:
                    item['qty'] = int(item['qty'])
                except (TypeError, ValueError):
                    item['qty'] = 1
                item['price'] = str(item['price'])
                continue
            needs_normalization[product_id] = item

        if not needs_normalization:
            return

        products = Product.objects.filter(id__in=needs_normalization.keys())
        product_map = {str(product.id): product for product in products}

        dirty = False
        for product_id, original in needs_normalization.items():
            product = product_map.get(product_id)
            if not product:
                self.basket.pop(product_id, None)
                dirty = True
                continue

            qty = original
            if isinstance(original, dict):
                qty = original.get('qty', 1)

            try:
                qty = int(qty)
            except (TypeError, ValueError):
                qty = 1

            self.basket[product_id] = {
                'price': str(product.price),
                'qty': max(qty, 1),
            }
            dirty = True

        if dirty:
            self.save()

    def add(self, product, qty):
        """
        Adding and updating the users basket session data
        """
        product_id = str(product.id)
        try:
            qty = int(qty)
        except (TypeError, ValueError):
            qty = 1

        if qty < 1:
            return

        if product_id not in self.basket:
            self.basket[product_id] = qty
        else:
            item = self.basket[product_id]
            if isinstance(item, dict):
                item['qty'] = int(item.get('qty', 0)) + qty
            else:
                item = {'price': str(product.price), 'qty': int(item) + qty}
            item['price'] = str(product.price)
            if item['qty'] < 1:
                item['qty'] = 1
            self.basket[product_id] = item

        self.save()

    def __iter__(self):
        """
        Collect the product-id in the session data to query the database
        and return products
        """
        product_ids = self.basket.keys()
        products = Product.objects.filter(id__in=product_ids)
        product_map = {str(product.id): product for product in products}

        for product_id in list(self.basket.keys()):
            product = product_map.get(product_id)
            if not product:
                continue

            item = self.get_item(product_id)
            if not item:
                continue

            yield {
                'product': product,
                'price': item['price'],
                'qty': item['qty'],
                'total_price': item['total_price'],
            }

    def __len__(self):
        """
        Get the basket data and count the qty of items
        """
        total_qty = 0
        for product_id in list(self.basket.keys()):
            item = self.get_item(product_id)
            if not item:
                continue
            total_qty += item['qty']
        return total_qty

    def update(self, product, qty):
        """
        Update values in session data
        """
        product_id = str(product)
        try:
            qty = int(qty)
        except (TypeError, ValueError):
            qty = 1

        if product_id in self.basket:
            if qty < 1:
                self.delete(product_id)
                return
            self.basket[product_id]['qty'] = qty

        self.save()

    def get_total_price(self):
        total = Decimal('0.00')
        for product_id in list(self.basket.keys()):
            item = self.get_item(product_id)
            if not item:
                continue
            total += item['total_price']
        return total

    def get_item(self, product):
        product_id = str(product if isinstance(product, (int, str)) else product.id)
        item = self.basket.get(product_id)
        if not item:
            return None

        product_obj = None

        if not isinstance(item, dict):
            product_obj = Product.objects.filter(id=product_id).first()
            if not product_obj:
                return None
            try:
                qty = int(item)
            except (TypeError, ValueError):
                qty = 1
            if qty < 1:
                qty = 1
            item = {'price': str(product_obj.price), 'qty': qty}
            self.basket[product_id] = item
            self.save()

        try:
            price = Decimal(item['price'])
        except (TypeError, ValueError, InvalidOperation):
            if product_obj is None:
                product_obj = Product.objects.filter(id=product_id).first()
            if not product_obj:
                return None
            price = Decimal(product_obj.price)
            item['price'] = str(product_obj.price)
            self.save()

        try:
            qty = int(item['qty'])
        except (TypeError, ValueError):
            qty = 1

        if qty < 1:
            qty = 1
            self.basket[product_id]['qty'] = qty
            self.save()

        return {
            'product_id': product_id,
            'price': price,
            'qty': qty,
            'total_price': price * qty,
        }

    def get_item_total(self, product):
        item = self.get_item(product)
        if not item:
            return Decimal('0.00')
        return item['total_price']

    def delete(self, product):
        """
        Delete item from session data
        """
        product_id = str(product if isinstance(product, (int, str)) else product.id)

        if product_id in self.basket:
            del self.basket[product_id]

        self.save()

    def save(self):

        self.session.modified = True