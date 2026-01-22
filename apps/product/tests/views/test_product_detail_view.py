from django.test import override_settings
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from ..factories import ProductFactory, UserFactory, CategoryFactory, BrandFactory


@override_settings(CACHES={'default': {'BACKEND': 'django.core.cache.backends.locmem.LocMemCache'}})
class ProductDetailAPIViewTest(APITestCase):
    """
    Integration tests for Product Detail, Update, and Deletion API.

    Ensures that:
    - Public users can only retrieve (GET) product details.
    - Only administrators can perform PUT, PATCH, and DELETE operations.
    - Service layer integrations for updates and deletions function correctly via HTTP.
    - Proper 404 and 403 errors are returned under unauthorized or invalid conditions.
    """

    def setUp(self):
        self.admin_user = UserFactory(is_staff=True)
        self.regular_user = UserFactory(is_staff=False)
        self.product = ProductFactory(name="Original Product")
        self.url = reverse('product:product-detail', kwargs={'pk': self.product.id})

    def test_get_product_detail_public(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], self.product.name)

    def test_update_product_as_admin_success(self):
        self.client.force_authenticate(user=self.admin_user)
        new_brand = BrandFactory()
        new_category = CategoryFactory()
        payload = {
            'name': 'Updated Product Name',
            'brand': new_brand.id,
            'category': new_category.id
        }
        response = self.client.put(self.url, payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'Updated Product Name')

    def test_partial_update_product_as_admin(self):
        self.client.force_authenticate(user=self.admin_user)
        payload = {'name': 'Patched Name'}
        response = self.client.patch(self.url, payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'Patched Name')

    def test_delete_product_as_admin(self):
        self.client.force_authenticate(user=self.admin_user)
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_unauthorized_modifications(self):
        self.client.force_authenticate(user=self.regular_user)

        # تست PUT
        self.assertEqual(self.client.put(self.url, {}).status_code, status.HTTP_403_FORBIDDEN)
        # تست DELETE
        self.assertEqual(self.client.delete(self.url).status_code, status.HTTP_403_FORBIDDEN)
