import factory
from apps.action.models.comment_model import Comment
from apps.post.tests.factories import PostFactory, UserFactory


class CommentFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Comment

    user = factory.SubFactory(UserFactory)
    post = factory.SubFactory(PostFactory)
    text = factory.Faker('paragraph')
    parent = None
