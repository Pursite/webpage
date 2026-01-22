# import pytest
# import os
# os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = "true"
# from rest_framework.test import APIClient
# from django.test import AsyncClient
# from pytest_factoryboy import register
# from apps.account.tests.factories import UserFactory
#
# register(UserFactory)
#
#
#
# @pytest.fixture
# def api_client():
#     return APIClient()
#
#
# @pytest.fixture
# def async_client():
#     return AsyncClient()
#
#
# @pytest.fixture
# def user_obj(db, user_factory):
#     return user_factory()
#
#
# @pytest.fixture
# def authenticated_client(api_client, user_obj):
#     api_client.force_authenticate(user=user_obj)
#     return api_client
#
#

