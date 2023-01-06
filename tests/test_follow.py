import re
import tempfile

import pytest
from django.contrib.auth import get_user_model
from django.core.paginator import Page
from django.db.models.fields.related import ForeignKey

try:
    from posts.models import Post
except ImportError:
    assert False, "Not found model post "

try:
    from posts.models import Follow
except ImportError:
    assert False, "Not found Follow model "


def search_field(model_fields, searching_field_name):
    for field in model_fields:
        if field.name == searching_field_name:
            return field
    return None


def search_refind(execution, user_code):
    """Search for launch"""
    for temp_line in user_code.split("\n"):
        if re.search(execution, temp_line):
            return True
    return False


class TestFollow:
    @pytest.mark.parametrize("field_name", ["following", "user"])
    def test_follow(self, field_name):
        model_name = "Follow"
        related_name = "follower" if field_name == "user" else "following_author"
        checking_field = search_field(Follow._meta.fields, field_name)
        field_in_model_text = f"Field `{field_name}` In the model `{model_name}`"
        assert (
            checking_field is not None
        ), f"{field_in_model_text} absent in the model or renamed. "
        assert isinstance(checking_field, ForeignKey), (
            f"{field_in_model_text} "
            "should be connected through the attitude of many-to-one "
            "With a model of users.Check the field class. "
        )
        assert checking_field.related_model == get_user_model(), (
            f"{field_in_model_text} should be connected with the model "
            f"`{get_user_model().__name__}`"
        )
        assert checking_field.remote_field.related_name == related_name, (
            f"{field_in_model_text} must contain " f"`related_name='{related_name}'`"
        )
        assert not checking_field.unique, (
            f"{field_in_model_text} "
            "Do not limit unique values."
            "A few can be signed for the same author "
            "readers.The same reader can be signed on "
            "Several authors."
        )
        assert checking_field.remote_field.on_delete.__name__ == "CASCADE", (
            f"{field_in_model_text} must provide " "`on_delete=models.CASCADE`."
        )

    def check_url(self, client, url, str_url):
        try:
            response = client.get(f"{url}")
        except Exception as e:
            assert False, f"""The page `{str_url}` works incorrectly.Mistake: `{e}`"""
        if response.status_code in (301, 302) and response.url == f"{url}/":
            response = client.get(f"{url}/")
        assert (
            response.status_code != 404
        ), f"Page `{str_url}` not found, check this address in *urls.py*"
        return response

    @pytest.mark.django_db(transaction=True)
    def test_follow_not_auth(self, client, user):
        response = self.check_url(client, "/follow", "/follow/")
        if not (
            response.status_code in (301, 302)
            and response.url.startswith("/auth/login")
        ):
            assert (
                False
            ), "Check that `/follow/` sends an authorized user to the authorization page "

        response = self.check_url(
            client, f"/profile/{user.username}/follow", "/profile/<username>/follow/"
        )
        if not (
            response.status_code in (301, 302)
            and response.url.startswith("/auth/login")
        ):
            assert False, (
                "Check that not an authorized user `Profile/<Username>/follow/` "
                "Send to the authorization page "
            )

        response = self.check_url(
            client,
            f"/profile/{user.username}/unfollow",
            "/profile/<username>/unfollow/",
        )
        if not (
            response.status_code in (301, 302)
            and response.url.startswith("/auth/login")
        ):
            assert False, (
                "Check that not an authorized user `Profile/<Username>/unfollow/` "
                "Send to the authorization page "
            )

    @pytest.mark.django_db(transaction=True)
    def test_follow_auth(self, user_client, user, post):
        assert hasattr(user, "follower"), (
            "The `user field in the` follow` model should contain "
            '`relatedName="follower"'
        )
        assert (
            user.follower.count() == 0
        ), "Check what subscriptions are considered correctly"
        self.check_url(
            user_client,
            f"/profile/{post.author.username}/follow",
            "/profile/<username>/follow/",
        )
        assert (
            user.follower.count() == 0
        ), "Check that you cannot subscribe to yourself "

        user_1 = get_user_model().objects.create_user(username="TestUser_2344")
        user_2 = get_user_model().objects.create_user(username="TestUser_73485")

        self.check_url(
            user_client,
            f"/profile/{user_1.username}/follow",
            "/profile/<username>/follow/",
        )
        assert user.follower.count() == 1, "Check that you can subscribe to the user "
        self.check_url(
            user_client,
            f"/profile/{user_1.username}/follow",
            "/profile/<username>/follow/",
        )
        assert (
            user.follower.count() == 1
        ), "Check that you can subscribe to the user only once "

        image = tempfile.NamedTemporaryFile(suffix=".jpg").name
        Post.objects.create(text="Test post 4564534", author=user_1, image=image)
        Post.objects.create(text="Test post 354745", author=user_1, image=image)

        Post.objects.create(text="Test post 245456", author=user_2, image=image)
        Post.objects.create(text="Test post 9789", author=user_2, image=image)
        Post.objects.create(text="Test post 4574", author=user_2, image=image)

        response = self.check_url(user_client, "/follow", "/follow/")
        assert (
            "page_obj" in response.context
        ), "Check that they transferred the variable `page_obj` to the context of the page`/follow/`"
        assert (
            type(response.context["page_obj"]) == Page
        ), "Check that the variable `page_obj` on the`/follow/`type` page` "
        assert (
            len(response.context["page_obj"]) == 2
        ), "Check that on the `/follow/` list of articles of the authors on which are signed "

        self.check_url(
            user_client,
            f"/profile/{user_2.username}/follow",
            "/profile/<username>/follow/",
        )
        assert user.follower.count() == 2, "Check that you can subscribe to the user "
        response = self.check_url(user_client, "/follow", "/follow/")
        assert (
            len(response.context["page_obj"]) == 5
        ), "Check that on the `/follow/` list of articles of the authors on which are signed "

        self.check_url(
            user_client,
            f"/profile/{user_1.username}/unfollow",
            "/profile/<username>/unfollow/",
        )
        assert (
            user.follower.count() == 1
        ), "Check that you can unsubscribe from the user "
        response = self.check_url(user_client, "/follow", "/follow/")
        assert (
            len(response.context["page_obj"]) == 3
        ), "Check that on the `/follow/` list of articles of the authors on which are signed "

        self.check_url(
            user_client,
            f"/profile/{user_2.username}/unfollow",
            "/profile/<username>/unfollow/",
        )
        assert (
            user.follower.count() == 0
        ), "Check that you can unsubscribe from the user "
        response = self.check_url(user_client, "/follow", "/follow/")
        assert (
            len(response.context["page_obj"]) == 0
        ), "Check that on the `/follow/` list of articles of the authors on which are signed "
