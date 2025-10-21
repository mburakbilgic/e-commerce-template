from decimal import Decimal

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from store.models import Category, Product


class BasketViewsTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username='tester',
            email='tester@example.com',
            password='pass1234',
        )
        self.category = Category.objects.create(name='Books', slug='books')
        self.product = Product.objects.create(
            category=self.category,
            created_by=self.user,
            title='Test Product',
            author='Tester',
            brand='Brand',
            summary='Summary',
            details='Details',
            slug='test-product',
            price=Decimal('19.99'),
        )

    def _add_to_basket(self, quantity=1):
        response = self.client.post(
            reverse('basket:basket_add'),
            {
                'productid': self.product.id,
                'productqty': quantity,
                'action': 'post',
            },
        )
        self.assertEqual(response.status_code, 200)
        return response

    def test_update_replaces_quantity(self):
        self._add_to_basket(quantity=2)

        response = self.client.post(
            reverse('basket:basket_update'),
            {
                'productid': self.product.id,
                'productqty': 5,
                'action': 'post',
            },
        )

        self.assertEqual(response.status_code, 200)
        payload = response.json()
        self.assertEqual(payload['item_qty'], 5)
        self.assertEqual(payload['removed'], False)

        basket_data = self.client.session['skey']
        self.assertEqual(int(basket_data[str(self.product.id)]['qty']), 5)

    def test_update_to_zero_removes_item(self):
        self._add_to_basket(quantity=3)

        response = self.client.post(
            reverse('basket:basket_update'),
            {
                'productid': self.product.id,
                'productqty': 0,
                'action': 'post',
            },
        )

        self.assertEqual(response.status_code, 200)
        payload = response.json()
        self.assertEqual(payload['removed'], True)
        self.assertEqual(payload['item_qty'], 0)
        self.assertEqual(self.client.session.get('skey', {}), {})

    def test_delete_removes_item(self):
        self._add_to_basket(quantity=2)

        response = self.client.post(
            reverse('basket:basket_delete'),
            {
                'productid': self.product.id,
                'action': 'post',
            },
        )

        self.assertEqual(response.status_code, 200)
        payload = response.json()
        self.assertEqual(payload['removed'], True)
        self.assertEqual(self.client.session.get('skey', {}), {})