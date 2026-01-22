import factory
from django.contrib.auth import get_user_model
from apps.product.models.product_model import Product, Category, Brand
from apps.post.models.post_model import Post

User = get_user_model()


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    username = factory.Faker('user_name')
    email = factory.Faker('email')
    password = factory.PostGenerationMethodCall('set_password', 'password123')


class CategoryFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Category

    title = factory.Sequence(lambda n: f'Category {n}')
    slug = factory.Sequence(lambda n: f'category-{n}')


class BrandFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Brand

    name = factory.Sequence(lambda n: f'Brand {n}')


class ProductFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Product

    user = factory.SubFactory(UserFactory)
    name = factory.Faker('word')
    category = factory.SubFactory(CategoryFactory)
    brand = factory.SubFactory(BrandFactory)


class PostFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Post

    product = factory.SubFactory(ProductFactory)
    user = factory.SubFactory(UserFactory)

    caption = factory.Faker('paragraph', nb_sentences=3)
    location = factory.Faker('city')

    price = factory.Iterator([100000, 250000, 500000, 1000000])
    is_active = True