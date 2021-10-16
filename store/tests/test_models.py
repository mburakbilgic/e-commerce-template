from django.contrib.auth.models import User
from django.test import TestCase
from django.urls.base import reverse

from store.models import Category, Product


class TestCategoriesModel(TestCase):

    def setUp(self):
        self.data1 = Category.objects.create(name='django', slug='django')

    def test_category_model_entry(self):
        """
        Test Category model data insertion/types/field attributes
        """
        data = self.data1
        self.assertTrue(isinstance(data, Category))
        self.assertEqual(str(data), 'django')
    
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
        Category.objects.create(name='django', slug='django')
        User.objects.create(username='admin')
        self.data1 = Product.objects.create(category_id=1, title='django', created_by_id=1,
                                            slug='django', price='20.00', image='django')

    def test_product_model_entry(self):
        """
        Test Product model data insertion/types/field attributes
        """
        data = self.data1
        self.assertTrue(isinstance(data, Product))
        self.assertEqual(str(data), 'django')
    
    def test_product_url(self):
        data = self.data1
        url = reverse('store:product_detail', args=[data.slug])
        self.assertEqual(url, '/django/')
        response = self.client.post(
            reverse('store:product_detail', args=[data.slug]))
        self.assertEqual(response.status_code, 200)