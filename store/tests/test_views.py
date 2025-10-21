from unittest import skip

from django.contrib.auth.models import User
from django.http.request import HttpRequest
from django.test import Client, RequestFactory, TestCase
from django.urls import reverse

from store.models import Category, Product
from store.views import product_all


@skip('demonstrating skipping')
class TestSkip(TestCase):

    def test_skip_example(self):
        pass


class TestViewResponses(TestCase):

    def setUp(self):
        self.c = Client()
        self.factory = RequestFactory()
        User.objects.create(username='admin')
        self.category = Category.objects.create(name='category', slug='s-category')
        Product.objects.create(
            category=self.category,
            title='products',
            created_by_id=1,
            slug='s-products',
            price='20.00',
            image='images',
        )

    def test_url_allowed_hosts(self):
        """
        Test allowed hosts
        """
        response = self.c.get('/', HTTP_HOST='noadress.com')
        self.assertEqual(response.status_code, 400)
        response = self.c.get('/', HTPP_HOST='yourdomain.com')
        self.assertEqual(response.status_code, 200)

    def test_product_detail_url(self):
        """
        Test Product response status
        """
        response = self.c.get(
            reverse(
                'store:product_detail',
                kwargs={'category_path': self.category.get_full_slug(), 'slug': 's-products'},
            )
        )
        self.assertEqual(response.status_code, 200)

    def test_category_detail_url(self):
        """
        Test Category response status
        """
        response = self.c.get(reverse('store:category_list', args=['s-category']))
        self.assertEqual(response.status_code, 200)

    def test_category_redirects_to_full_slug(self):
        parent = Category.objects.create(name='Parent', slug='parent')
        child = Category.objects.create(name='Child', slug='child', parent=parent)

        response = self.c.get(reverse('store:category_list', args=[child.slug]))
        self.assertEqual(response.status_code, 301)
        self.assertEqual(
            response.headers['Location'],
            reverse('store:category_list', args=[child.get_full_slug()])
        )

    def test_legacy_product_slug_redirects_to_canonical_path(self):
        product = Product.objects.get(slug='s-products')
        response = self.c.get(reverse('store:product_detail_legacy', args=['s-products']))
        self.assertEqual(response.status_code, 301)
        self.assertEqual(
            response.headers['Location'],
            reverse(
                'store:product_detail',
                kwargs={
                    'category_path': product.category.get_full_slug(),
                    'slug': product.slug,
                },
            ),
        )

    def test_homepage_html(self):
        request = HttpRequest()
        response = product_all(request)
        html = response.content.decode('utf8')
        self.assertIn('<title>Black Market</title>', html)
        self.assertTrue(html.startswith('\n<!DOCTYPE html>\n'))
        self.assertEqual(response.status_code, 200)

    def test_view_function(self):
        request = self.factory.get('/s-products')
        response = product_all(request)
        html = response.content.decode('utf8')
        self.assertIn('<title>Black Market</title>', html)
        self.assertTrue(html.startswith('\n<!DOCTYPE html>\n'))
        self.assertEqual(response.status_code, 200)
