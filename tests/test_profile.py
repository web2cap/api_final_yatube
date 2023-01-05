import pytest
from django.contrib.auth import get_user_model
from django.core.paginator import Page

from tests.utils import get_field_from_context


class TestProfileView:

    @pytest.mark.django_db(transaction=True)
    def test_profile_view_get(self, client, post_with_group):
        url = f'/profile/{post_with_group.author.username}'
        url_templ = '/profile/<username>/'
        try:
            response = client.get(url)
        except Exception as e:
            assert False, f'''The page `{url_templ}` works incorrectly.Error: `{e}`'''
        if response.status_code in (301, 302):
            response = client.get(f'{url}/')
        assert response.status_code != 404, (
            f'Page `{url_templ}` not found, check this address in *urls.py *'
        )

        profile_context = get_field_from_context(response.context, get_user_model())
        assert profile_context is not None, f'Check what the author handed over to the context of the page `{url_templ}` '

        page_context = get_field_from_context(response.context, Page)
        assert page_context is not None, (
            f'Check what you transferred to the author’s articles to the context of the page `{url_templ}` like `page` '
        )
        assert len(page_context.object_list) == 1, (
            f'Check that the right articles of the author `{url_templ}`  are transferred to the context of the page.'
        )
        posts_list = page_context.object_list
        for post in posts_list:
            assert hasattr(post, 'image'), (
                f'Make sure that the article transmitted to the context of the page `{url_templ}` has a field `image` '
            )
            assert getattr(post, 'image') is not None, (
                f'Make sure that the article transmitted to the context of the page `{url_templ}` has a field `Image`, '
                'And the image is transmitted there '
            )

        new_user = get_user_model()(username='new_user_87123478')
        new_user.save()
        url = f'/profile/{new_user.username}'
        try:
            new_response = client.get(url)
        except Exception as e:
            assert False, f'''The page `{url_templ}` works incorrectly. Mistake: `{e}`'''
        if new_response.status_code in (301, 302):
            new_response = client.get(f'{url}/')

        page_context = get_field_from_context(new_response.context, Page)
        assert page_context is not None, (
            f'Check what you transferred to the author’s articles to the context of the page `{url_templ}` like `page` '
        )
        assert len(page_context.object_list) == 0, (
            f'Check that the author’s correct articles in the context of the page `{url_templ}` '
        )
