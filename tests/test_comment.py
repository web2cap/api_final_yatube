import re

import pytest
from django.contrib.auth import get_user_model
from django.db.models import fields

try:
    from posts.models import Comment
except ImportError:
    assert False, "Not found model Comment "

try:
    from posts.models import Post
except ImportError:
    assert False, "Not found model post "


def search_field(fields, attname):
    for field in fields:
        if attname == field.attname:
            return field
    return None


def search_refind(execution, user_code):
    """searchForLaunch"""
    for temp_line in user_code.split("\n"):
        if re.search(execution, temp_line):
            return True
    return False


class TestComment:
    def test_comment_model(self):
        model_fields = Comment._meta.fields
        text_field = search_field(model_fields, "text")
        assert (
            text_field is not None
        ), "Add the name of the event `Text` Model` Comment` "
        assert (
            type(text_field) == fields.TextField
        ), "Property `Text` Models` Comment` should be textual `TextField` "

        pub_date_field_name = "created"
        pub_date_field = search_field(model_fields, "pub_date")
        if pub_date_field is not None:
            pub_date_field_name = "pub_date"
        else:
            pub_date_field = search_field(model_fields, "created")
            if pub_date_field is not None:
                pub_date_field_name = "created"

        assert (
            pub_date_field is not None
        ), f"Add the date and time of the event `{pub_date_field_name}` Model `Comment` "
        assert (
            type(pub_date_field) == fields.DateTimeField
        ), f"Property {pub_date_field_name} `Model` Comment` should be the date and time of `DATETIMEFILD` "
        assert (
            pub_date_field.auto_now_add
        ), f"Property {pub_date_field_name} `Model` Comment` should be `auto_now_add` "

        author_field = search_field(model_fields, "author_id")
        assert (
            author_field is not None
        ), "Add a user, an author who created an event `Author` Model` Comment` "
        assert (
            type(author_field) == fields.related.ForeignKey
        ), "The property of `author` Models` Comment` should be a link to another model `Foreignkey` "
        assert (
            author_field.related_model == get_user_model()
        ), "Property `Author` Models` Comment` should be a link to the user model `user` "

        post_field = search_field(model_fields, "post_id")
        assert post_field is not None, "Add the `Group` property to the` comment` "
        assert (
            type(post_field) == fields.related.ForeignKey
        ), "The property of `Group` Models` Comment` should be a link to another model `Foreignkey` "
        assert (
            post_field.related_model == Post
        ), "Property `Group` Model` Comment` should be a link to the `Post` model "

    @pytest.mark.django_db(transaction=True)
    def test_comment_add_view(self, client, post):
        try:
            response = client.get(f"/posts/{post.id}/comment")
        except Exception as e:
            assert (
                False
            ), f"""The `/posts/<Post_ID>/comment/` page works incorrectly.Error: `{e}` """
        if (
            response.status_code in (301, 302)
            and response.url == f"/posts/{post.id}/comment/"
        ):
            url = f"/posts/{post.id}/comment/"
        else:
            url = f"/posts/{post.id}/comment"
        assert (
            response.status_code != 404
        ), "Page `/Posts/<Post_id>/comment/` Not found, check this address in *urls.py *"

        response = client.post(url, data={"text": "Новый коммент!"})
        if not (
            response.status_code in (301, 302)
            and response.url.startswith("/auth/login")
        ):
            assert False, (
                "Check that not an authorized user "
                "`/posts/<Post_id>/comment/` Send to the authorization page "
            )

    @pytest.mark.django_db(transaction=True)
    def test_comment_add_auth_view(self, user_client, post):
        try:
            response = user_client.get(f"/posts/{post.id}/comment")
        except Exception as e:
            assert (
                False
            ), f"""The `/posts/<Post_ID>/comment/` page works incorrectly.Mistake:`{e}`"""
        if (
            response.status_code in (301, 302)
            and response.url == f"/posts/{post.id}/comment/"
        ):
            url = f"/posts/{post.id}/comment/"
        else:
            url = f"/posts/{post.id}/comment"
        assert (
            response.status_code != 404
        ), "Page `/Posts/<Post_id>/comment/` Not found, check this address in *urls.py *"

        text = "New comment 94938!"
        response = user_client.post(url, data={"text": text})

        assert response.status_code in (301, 302), (
            "Check what from the page `/posts/<Post_id>/comment/` "
            "After creating the comment, redirect the post page "
        )
        comment = Comment.objects.filter(
            text=text, post=post, author=post.author
        ).first()
        assert (
            comment is not None
        ), "Check that you are creating a new comment `/posts/<Post_id>/comment/` "
        assert response.url.startswith(f"/posts/{post.id}"), (
            "Check what you redirect to the post page"
            "`/posts/<Post_id>/` after adding a new comment "
        )
