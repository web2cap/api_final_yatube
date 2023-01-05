import pytest


@pytest.fixture
def user(django_user_model):
    return django_user_model.objects.create_user(username='TestUser', password='1234567')

@pytest.fixture
def user_2(django_user_model):
    return django_user_model.objects.create_user(username='TestUser2', password='1234567')


@pytest.fixture
def another_user(django_user_model):
    return django_user_model.objects.create_user(username='TestUserAnother', password='1234567')

@pytest.fixture
def token(user):
    from rest_framework_simplejwt.tokens import RefreshToken
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }


#TODO: Rename in tests
@pytest.fixture
def user_api_client(token):
    from rest_framework.test import APIClient

    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION=f'Bearer {token["access"]}')
    return client

@pytest.fixture
def user_client(user, client):
    client.force_login(user)
    return client


@pytest.fixture
def another_user(mixer):
    from django.contrib.auth.models import User
    return mixer.blend(User, username='AnotherUser')
