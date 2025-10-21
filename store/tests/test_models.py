from django.contrib.auth.models import User
from django.test import TestCase
from django.urls.base import reverse

from store.models import Category, Product


class TestCategoriesModel(TestCase):

    def setUp(self):
        self.data1 = Category.objects.create(name='example category', slug='example-category')

    def test_category_model_entry(self):
        """
        Test Category model data insertion/types/field attributes
        """
        data = self.data1
        self.assertTrue(isinstance(data, Category))
        self.assertEqual(str(data), 'example category')

    def test_category_urL(self):
        """
        Test category model slug and URL reverse
        """
        data = self.data1
        response = self.client.post(
            reverse('store:category_list', args=[data.slug]))
        self.assertEqual(response.status_code, 200)


class TestProductsModel(TestCase):

    def setUp(self):
        self.category = Category.objects.create(name='category', slug='s-category')
        User.objects.create(username='admin')
        self.data1 = Product.objects.create(
            category=self.category,
            title='products',
            created_by_id=1,
            slug='s-products',
            price='20.00',
            image='images',
        )

    def test_product_model_entry(self):
        """
        Test Product model data insertion/types/field attributes
        """
        data = self.data1
        self.assertTrue(isinstance(data, Product))
        self.assertEqual(str(data), 'products')

    def test_product_url(self):
        data = self.data1
        url = reverse(
            'store:product_detail',
            kwargs={
                'category_path': data.category.get_full_slug(),
                'slug': data.slug,
            },
        )
        self.assertEqual(url, '/shop/s-category/s-products/')
        response = self.client.post(url)
