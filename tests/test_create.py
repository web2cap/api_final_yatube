from io import BytesIO

import pytest
from django import forms
from django.core.files.base import File
from PIL import Image
from posts.models import Post


class TestCreateView:
    @pytest.mark.django_db(transaction=True)
    def test_create_view_get(self, user_client):
        try:
            response = user_client.get("/create/")
        except Exception as e:
            assert False, f"""The `/Create/` page works incorrectly.Mistake: `{e}`"""
        if response.status_code in (301, 302):
            response = user_client.get("/create/")
        assert (
            response.status_code != 404
        ), "Page `/Create/` Not found, check this address in *urls.py *"
        assert (
            "form" in response.context
        ), "Check that they conveyed the form `Form` to the context of the page`/Create/`"
        fields_cnt = 3
        assert (
            len(response.context["form"].fields) == fields_cnt
        ), f"Check that in the form of `Form` on the page`/Create/`{fields_cnt} Fields"
        assert (
            "group" in response.context["form"].fields
        ), "Check that in the form of `Form` on the`/Create/`there is a field` Group` "
        assert (
            type(response.context["form"].fields["group"])
            == forms.models.ModelChoiceField
        ), "Check that in the form of `Form` on the`/Create/`Field` Group` type `modelchoicefield` "
        assert (
            not response.context["form"].fields["group"].required
        ), "Check that in the form of `Form` on the`/Create/`field` Group` is not necessary "

        assert (
            "text" in response.context["form"].fields
        ), "Check that in the form of `Form` on the`/Create/`there is a field` text` "
        assert (
            type(response.context["form"].fields["text"]) == forms.fields.CharField
        ), "Check that in the form of `Form` on the`/Create/`Field` Text type `charfield`"
        assert (
            response.context["form"].fields["text"].required
        ), "Check that in the form of `Form` on the`/Create/`Field` Text "

        assert (
            "image" in response.context["form"].fields
        ), "Check that in the form of `Form` on the`/Create/`there is a field` Image` "
        assert (
            type(response.context["form"].fields["image"]) == forms.fields.ImageField
        ), "Check that in the form of `Form` on the`/Create/`field` Image type `imagefield`"

    @staticmethod
    def get_image_file(name, ext="png", size=(50, 50), color=(256, 0, 0)):
        file_obj = BytesIO()
        image = Image.new("RGBA", size=size, color=color)
        image.save(file_obj, ext)
        file_obj.seek(0)
        return File(file_obj, name=name)

    @pytest.mark.django_db(transaction=True)
    def test_create_view_post(self, mock_media, user_client, user, group):
        text = "Checking a new post!"
        try:
            response = user_client.get("/create")
        except Exception as e:
            assert False, f"""The `/Create` page works incorrectly.Mistake: `{e}`"""
        url = "/create/" if response.status_code in (301, 302) else "/create"

        image = self.get_image_file("image.png")
        response = user_client.post(
            url, data={"text": text, "group": group.id, "image": image}
        )

        assert response.status_code in (301, 302), (
            "Check what from the page `/Create/` after creating a post, "
            f"redirect the author `/propile/{user.username}`  to the profile page of the author"
        )
        post = Post.objects.filter(author=user, text=text, group=group).first()
        assert (
            post is not None
        ), "Check that you have saved a new post when sending a form on the `/Create/` page"
        assert (
            response.url == f"/profile/{user.username}/"
        ), f"Check what you redirect to the profile page of the author `/profile/{user.username}` "

        text = "Checking a new post 2!"
        image = self.get_image_file("image2.png")
        response = user_client.post(url, data={"text": text, "image": image})
        assert response.status_code in (301, 302), (
            "Check what from the page `/Create/` after creating a post, "
            f"redirect the author `/propile/{user.username}`  to the profile page of the author"
        )
        post = Post.objects.filter(author=user, text=text, group__isnull=True).first()
        assert (
            post is not None
        ), "Check that you have saved a new post when sending a form on the `/Create/` page"
        assert (
            response.url == f"/profile/{user.username}/"
        ), f"Check what you redirect to the profile page of the author `/profile/{user.username}` "

        response = user_client.post(url)
        assert (
            response.status_code == 200
        ), "Check that on the `/Create/` take errors with an incorrect completed form `Form` "
