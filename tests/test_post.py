from io import BytesIO

import pytest
from django import forms
from django.contrib.auth import get_user_model
from django.core.cache import cache
from django.core.files.base import File
from django.core.paginator import Page
from django.db.models.query import QuerySet
from PIL import Image
from posts.forms import PostForm
from posts.models import Post

from tests.utils import get_field_from_context


class TestPostView:
    @pytest.mark.django_db(transaction=True)
    def test_index_post_with_image(self, client, post):
        url_index = "/"
        cache.clear()
        response = client.get(url_index)

        page_context = get_field_from_context(response.context, Page)
        assert (
            page_context is not None
        ), "Check what you transferred to the author’s articles to the context of the main page `/` like `page` "
        assert (
            len(page_context.object_list) == 1
        ), "Check that the author’s correct articles are transferred to the context of the main page "
        posts_list = page_context.object_list
        for post in posts_list:
            assert hasattr(
                post, "image"
            ), "Make sure that the article transmitted to the context of the main page `/` has a field `Image` "
            assert getattr(post, "image") is not None, (
                "Make sure that the article transmitted to the context of the main page `/` has a field `Image`, "
                "And the image is transmitted there "
            )

    @pytest.mark.django_db(transaction=True)
    def test_index_post_caching(self, client, post, post_with_group):
        url_index = "/"
        cache.clear()
        response = client.get(url_index)

        page_context = get_field_from_context(response.context, Page)
        assert (
            page_context is not None
        ), "Check what you transferred to the author’s articles to the context of the main page `/` like `page` "
        posts_cnt = Post.objects.count()
        post.delete()
        assert len(page_context.object_list) == posts_cnt is not None, (
            "Check what you set up caching for the main page `/` "
            "and posts on it even when removing in the database, remain until the cache is cleaned "
        )
        cache.clear()
        posts_cnt = Post.objects.count()
        response = client.get(url_index)
        page_context = get_field_from_context(response.context, Page)
        assert len(page_context.object_list) == posts_cnt is not None, (
            "Check what you set up caching for the main page `/` "
            "And with a forced cleaning of the cache, a post remote in the database, "
            "disappears from the cache "
        )

    @pytest.mark.django_db(transaction=True)
    def test_post_view_get(self, client, post_with_group):
        try:
            response = client.get(f"/posts/{post_with_group.id}")
        except Exception as e:
            assert (
                False
            ), f"""The `/posts/<Post_id>/` page works incorrectly.Mistake: `{e}`"""
        if response.status_code in (301, 302):
            response = client.get(f"/posts/{post_with_group.id}/")
        assert (
            response.status_code != 404
        ), "Page `/Posts/<Post_id>/` Not found, check this address in *urls.py *"

        post_context = get_field_from_context(response.context, Post)
        assert (
            post_context is not None
        ), "Check what you transferred to the article to the context of the `/posts/<Post_ID>/` type `post` page"

        try:
            from posts.forms import CommentForm
        except ImportError:
            assert False, "No CommentForm form in Posts.Form "

        comment_form_context = get_field_from_context(response.context, CommentForm)
        assert (
            comment_form_context is not None
        ), "Check that they conveyed the form of comment to the context of the page `/posts/<Post_id>/` like `commentForm` "
        assert (
            len(comment_form_context.fields) == 1
        ), "Check that the form of commentary in the context of the page `/posts/<Post_id>/` consists of one field "
        assert (
            "text" in comment_form_context.fields
        ), "Check that the form of commentary in the context of the page `/posts/<Post_id>/` contains the `Text` field"
        assert type(comment_form_context.fields["text"]) == forms.fields.CharField, (
            "Check that the form of commentary in the context of the page `/posts/<Post_id>/` "
            "Contained `Text` type` charfield` "
        )
        assert hasattr(
            post_context, "image"
        ), "Make sure that the article transmitted to the context of the page `/posts/<Post_id>/` has a field `Image` "
        assert getattr(post_context, "image") is not None, (
            "Make sure that the article transmitted to the context of the page `/posts/<Post_id>/` has a field `Image`, "
            "And the image is transmitted there "
        )


class TestPostEditView:
    @pytest.mark.django_db(transaction=True)
    def test_post_edit_view_get(self, client, post_with_group):
        try:
            response = client.get(f"/posts/{post_with_group.id}/edit")
        except Exception as e:
            assert (
                False
            ), f"""Страница `/posts/<post_id>/edit/` работает неправильно. Ошибка: `{e}`"""
        if response.status_code in (301, 302) and not response.url.startswith(
            f"/posts/{post_with_group.id}"
        ):
            response = client.get(f"/posts/{post_with_group.id}/edit/")
        assert (
            response.status_code != 404
        ), "Страница `/posts/<post_id>/edit/` не найдена, проверьте этот адрес в *urls.py*"

        assert response.status_code in (301, 302), (
            "Проверьте, что вы переадресуете пользователя со страницы "
            "`/posts/<post_id>/edit/` на страницу поста, если он не автор"
        )

    @pytest.mark.django_db(transaction=True)
    def test_post_edit_view_author_get(self, user_client, post_with_group):
        try:
            response = user_client.get(f"/posts/{post_with_group.id}/edit")
        except Exception as e:
            assert (
                False
            ), f"""Страница `/posts/<post_id>/edit/` работает неправильно. Ошибка: `{e}`"""
        if response.status_code in (301, 302):
            response = user_client.get(f"/posts/{post_with_group.id}/edit/")
        assert (
            response.status_code != 404
        ), "Page `/Posts/<Post_id>/edit/` Not found, check this address in *urls.py *"

        post_context = get_field_from_context(response.context, Post)
        postform_context = get_field_from_context(response.context, PostForm)
        assert (
            any([post_context, postform_context]) is not None
        ), "Check what you handed over to the context of the page `/posts/<Post_ID>/edit/` like `post` or` postform` "

        assert (
            "form" in response.context
        ), "Check that they conveyed the form `Form` to the context of the page`/posts/<Post_id>/edit/`"
        fields_cnt = 3
        assert (
            len(response.context["form"].fields) == fields_cnt
        ), f"Check that in the form of `Form` on the page`/posts/<Post_id>/edit/`{fields_cnt} Fields"
        assert (
            "group" in response.context["form"].fields
        ), "Check that in the form of `Form` on the`/Posts/<Post_ID>/edit/`there is a field` Group` "
        assert (
            type(response.context["form"].fields["group"])
            == forms.models.ModelChoiceField
        ), "Check that in the form of `Form` on the`/Posts/<Post_ID>/edit/`field` Group` type `modelchoicefield` "
        assert (
            not response.context["form"].fields["group"].required
        ), "Check that in the form of `Form` on the page`/posts/<Post_id>/edit/`` Group` field is not necessarily "

        assert (
            "text" in response.context["form"].fields
        ), "Check that in the form of `Form` on the`/Posts/<Post_ID>/edit/`there is a field` text` "
        assert (
            type(response.context["form"].fields["text"]) == forms.fields.CharField
        ), "Check that in the form of `Form` on the`/Posts/<Post_ID>/edit/`field` text` type `charfield` "
        assert (
            response.context["form"].fields["text"].required
        ), "Check that in the form of `Form` on the page`/posts/<Post_ID>/edit/`Field` Group`"

        assert (
            "image" in response.context["form"].fields
        ), "Check that in the form of `Form` on the`/Posts/<Post_ID>/edit/`there is a field` Image` "
        assert (
            type(response.context["form"].fields["image"]) == forms.fields.ImageField
        ), "Check that in the form of `Form` on the`/Posts/<Post_ID>/edit/`` Image` type `imagefield` "

    @staticmethod
    def get_image_file(name, ext="png", size=(50, 50), color=(256, 0, 0)):
        file_obj = BytesIO()
        image = Image.new("RGBA", size=size, color=color)
        image.save(file_obj, ext)
        file_obj.seek(0)
        return File(file_obj, name=name)

    @pytest.mark.django_db(transaction=True)
    def test_post_edit_view_author_post(self, mock_media, user_client, post_with_group):
        text = "Checking the post!"
        try:
            response = user_client.get(f"/posts/{post_with_group.id}/edit")
        except Exception as e:
            assert (
                False
            ), f"""The `/posts/<Post_ID>/edit/` page works incorrectly.Mistake: `{e}`"""
        url = (
            f"/posts/{post_with_group.id}/edit/"
            if response.status_code in (301, 302)
            else f"/posts/{post_with_group.id}/edit"
        )

        image = self.get_image_file("image2.png")
        response = user_client.post(
            url, data={"text": text, "group": post_with_group.group_id, "image": image}
        )

        assert response.status_code in (301, 302), (
            "Check what from the page `/posts/<Post_id>/edit/` "
            "After creating the post, redirect the post page "
        )
        post = Post.objects.filter(
            author=post_with_group.author, text=text, group=post_with_group.group
        ).first()
        assert (
            post is not None
        ), "Check that you have changed the post when sending a form on the `/posts/<Post_ID>/edit/` page"
        assert response.url.startswith(
            f"/posts/{post_with_group.id}"
        ), "Check what you redirect to the page `/posts/<Post_id>/` "
