from django.core.files.uploadedfile import SimpleUploadedFile
from django.db import IntegrityError
from django.test import TestCase, override_settings
from ..factories import ProductFactory, BrandFactory, CategoryFactory, UserFactory, ProductImageFactory
from ...models.product_image_model import ProductImage
import os


@override_settings(CACHES={'default': {'BACKEND': 'django.core.cache.backends.locmem.LocMemCache'}})
class ProductImageModelTest(TestCase):
    """
        Test suite for the ProductImage model.

        Covers integrity constraints (unique_together for featured images),
        default field values, and custom dynamic upload paths including
        UUID renaming for security and organization.
    """

    def setUp(self):
        self.brand = BrandFactory(name="Samsung")
        self.category = CategoryFactory(title="Mobile")
        self.user = UserFactory()

    def test_product_image_unique_feature_constraint(self):
        product = ProductFactory()
        ProductImageFactory(product=product, image="test1.jpg", is_feature=True)

        with self.assertRaises(IntegrityError):
            ProductImageFactory(product=product, image="test2.jpg", is_feature=True)

    def test_product_image_default_is_feature(self):
        product = ProductFactory()
        img = ProductImageFactory(product=product, image="test.jpg")
        self.assertFalse(img.is_feature)

    def test_product_image_str(self):
        product = ProductFactory(name="Test Product")
        image = ProductImageFactory(product=product, image="test.jpg")
        self.assertEqual(str(image), "Image for Test Product")

    def test_product_image_upload_path(self):
        product = ProductFactory()
        small_gif = (
            b'\x47\x49\x46\x38\x39\x61\x01\x00\x01\x00\x80\x00\x00\xff\xff\xff'
            b'\xff\xff\xff\x21\xf9\x04\x01\x00\x00\x00\x00\x2c\x00\x00\x00\x00'
            b'\x01\x00\x01\x00\x00\x02\x02\x44\x01\x00\x3b'
        )
        fake_image = SimpleUploadedFile("pixel.gif", small_gif, content_type="image/gif")

        obj = ProductImage.objects.create(product=product, image=fake_image)

        expected_path_part = f"products/product_{product.id}/"
        self.assertIn(expected_path_part, obj.image.name)

        filename = os.path.basename(obj.image.name)
        name_without_ext = filename.split('.')[0]
        self.assertEqual(len(name_without_ext), 36)
