import factory
from django.contrib.auth.models import User
from apps.product.models.category_brand_model import Brand, Category
from apps.product.models.product_image_model import ProductImage
from apps.product.models.product_model import Product


class UserFactory(factory.django.DjangoModelFactory):
    """
        Factory for Django's built-in User model.
        Generates unique usernames and default non-staff users.
    """

    class Meta:
        model = User

    username = factory.Faker('user_name')
    is_staff = False


class BrandFactory(factory.django.DjangoModelFactory):
    """
        Factory for the Brand model.
        Produces random company names for product branding.
    """

    class Meta:
        model = Brand

    name = factory.Faker('company')


class CategoryFactory(factory.django.DjangoModelFactory):
    """
        Factory for the Category model.
        Includes unique slug generation to prevent integrity errors.
    """

    class Meta:
        model = Category

    title = factory.Faker('word')
    slug = factory.Faker('slug')


class ProductFactory(factory.django.DjangoModelFactory):
    """
        Factory for the Product model.
        Automatically handles related User, Brand, and Category instances.
    """

    class Meta:
        model = Product

    user = factory.SubFactory(UserFactory)
    name = factory.Faker('text')
    brand = factory.SubFactory(BrandFactory)
    category = factory.SubFactory(CategoryFactory)


class ProductImageFactory(factory.django.DjangoModelFactory):
    """
        Factory for the ProductImage model.
        Handles mock image file names and ensures default is_feature is False.
    """

    class Meta:
        model = ProductImage

    product = factory.SubFactory(ProductFactory)
    image = factory.Faker('file_name', extension='jpg')
    is_feature = False
