import pytest
from django.core.cache import cache
from django.core.paginator import Page, Paginator

pytestmark = [pytest.mark.django_db]

class TestGroupPaginatorView:

    def test_group_paginator_view_get(self, client, few_posts_with_group):
        try:
            response = client.get(f'/group/{few_posts_with_group.group.slug}')
        except Exception as e:
            assert False, f'''The `/Group/<Slug>/` page works incorrectly.Mistake: `{e}`'''
        if response.status_code in (301, 302):
            response = client.get(f'/group/{few_posts_with_group.group.slug}/')
        assert response.status_code != 404, 'Page `/Group/<Slug>/` Not found, check this address in *urls.py *'
        assert 'page_obj' in response.context, (
            'Check that they transferred the variable `page_obj` to the context of the page`/group/<SLUG>/`'
        )
        assert isinstance(response.context['page_obj'], Page), (
            'Check that the variable `page_obj` on the`/Group/<Slug>/`type` page` '
        )

    def test_group_paginator_not_in_context_view(self, client, post_with_group):
        response = client.get(f'/group/{post_with_group.group.slug}/')
        assert response.status_code != 404, 'Page `/Group/<Slug>/` Not found, check this address in *urls.py *'
        assert isinstance(response.context['page_obj'].paginator, Paginator), (
            'Check that the variable `paginator` on the`/Group/<Slug>/`type` paginator` '
        )

    def test_index_paginator_not_in_view_context(self, client, few_posts_with_group):
        response = client.get('/')
        assert isinstance(response.context['page_obj'].paginator, Paginator), (
            'Check that the variable `paginator` object` page_obj` on the `/` type `paginator` page'
        )

    def test_index_paginator_view(self, client, post_with_group):
        cache.clear()
        response = client.get('/')
        assert response.status_code != 404, 'Page `/` not found, check this address in *urls.py *'
        assert 'page_obj' in response.context, (
            'Check what you handed over the variable `page_obj` in the context of the page`/`'
        )
        assert isinstance(response.context['page_obj'], Page), (
            'Check that the variable `page_obj` on the page`/`like` page` '
        )

    def test_profile_paginator_view(self, client, few_posts_with_group):
        response = client.get(f'/profile/{few_posts_with_group.author.username}/')
        assert isinstance(response.context['page_obj'].paginator, Paginator), (
            'Check that the variable `paginator` object` page_obj` '
            'to pages `/ Profile / <username> /` Type `paginator` '
        )
