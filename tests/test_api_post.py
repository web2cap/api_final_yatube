import pytest
from posts.models import Post


class TestPostAPI:
    @pytest.mark.django_db(transaction=True)
    def test_post_not_found(self, client, post):
        response = client.get("/api/v1/posts/")

        assert (
            response.status_code != 404
        ), "Page `/API/V1/Posts/` Not found, check this address in *urls.py *"

    @pytest.mark.django_db(transaction=True)
    def test_post_list_not_auth(self, client, post):
        response = client.get("/api/v1/posts/")

        assert (
            response.status_code == 200
        ), "Check that on `/API/V1/Posts/` when requesting without token, return the status of 200 "

    @pytest.mark.django_db(transaction=True)
    def test_post_single_not_auth(self, client, post):
        response = client.get(f"/api/v1/posts/{post.id}/")

        assert (
            response.status_code == 200
        ), "Check that on `/API/V1/Posts/{post.id}/` when requesting without token, return the status of 200 "

    @pytest.mark.django_db(transaction=True)
    def test_posts_get_not_paginated(self, user_api_client, post, another_post):
        response = user_api_client.get("/api/v1/posts/")
        assert (
            response.status_code == 200
        ), "Check that when a GET request is `/API/V1/Posts/` with an authorization token status 200 returns"

        test_data = response.json()

        # response without pagination must be a list type
        assert (
            type(test_data) == list
        ), "Check that with a GET request on `/API/V1/Posts/` without pagination, the list is returned "

        assert (
            len(test_data) == Post.objects.count()
        ), "Check that when a GET request on `/API/V1/Posts/` The entire list of articles is returned without pagination."

        post = Post.objects.all()[0]
        test_post = test_data[0]
        assert (
            "id" in test_post
        ), "Check that they added `ID` to the` Fields` field of the POST model serializer "
        assert (
            "text" in test_post
        ), "Check that they added `Text` to the` Fields` field of the POST model serializer "
        assert (
            "author" in test_post
        ), "Check that they added `Author` to the` Fields` Fields Severizer of the POST Model"
        assert (
            "pub_date" in test_post
        ), "Check that you added `Pub_Date` to the` Fields` field of the POST model serializer "
        assert (
            test_post["author"] == post.author.username
        ), "Check that `Author` of the POST model returns the users name "

        assert (
            test_post["id"] == post.id
        ), "Check that when a GET request on `/API/V1/Posts/` the entire list of articles is returned "

    @pytest.mark.django_db(transaction=True)
    def test_posts_get_paginated(self, user_api_client, post, post_2, another_post):
        base_url = "/api/v1/posts/"
        limit = 2
        offset = 2
        url = f"{base_url}?limit={limit}&offset={offset}"
        response = user_api_client.get(url)
        assert (
            response.status_code == 200
        ), f"Check that when a GET request is `{url}` with an authorization token status 200 returns"

        test_data = response.json()
        assert (
            type(test_data) == dict
        ), f"Check that when a GET request is `{url}` with pagination, the dictionary is returned "
        assert (
            "results" in test_data.keys()
        ), f"Make sure that with a GET request on `{url}` with pagination, the key `results` is present in the answer "
        assert (
            len(test_data.get("results")) == Post.objects.count() - offset
        ), f"Check that with a GET request on `{url}` with pagination, the correct number of articles is returned "
        assert test_data.get("results")[0].get("text") == post.text, (
            f"Make sure that with a GET request on `{url}` with pagination, "
            "The answer contains correct articles"
        )

        test_post = test_data.get("results")[0]
        assert (
            "id" in test_post
        ), "Check that they added `ID` to the` Fields` field of the POST model serializer "
        assert (
            "text" in test_post
        ), "Check that they added `Text` to the` Fields` field of the POST model serializer "
        assert (
            "author" in test_post
        ), "Check that they added `Author` to the` Fields` Fields Severizer of the POST Model"
        assert (
            "pub_date" in test_post
        ), "Check that you added `Pub_Date` to the` Fields` field of the POST model serializer "
        assert (
            test_post["author"] == post.author.username
        ), "Check that `Author` of the POST model returns the users name "

        assert (
            test_post["id"] == post.id
        ), f"Check that when a GET request on `{url}` the correct list of articles is returned"

    @pytest.mark.django_db(transaction=True)
    def test_post_create(self, user_api_client, user, another_user, group_1):
        post_count = Post.objects.count()

        data = {}
        response = user_api_client.post("/api/v1/posts/", data=data)
        assert (
            response.status_code == 400
        ), "Check that when posting at `/API/V1/POSTS/` With the wrong data, status 400 is returned"

        data = {"text": "Статья номер 3"}
        response = user_api_client.post("/api/v1/posts/", data=data)
        assert (
            response.status_code == 201
        ), "Check that when posting at `/API/V1/Posts/` Status 201 returns the correct data with the correct data"
        assert (
            response.json().get("author") is not None
            and response.json().get("author") == user.username
        ), (
            "Check that when posting at `/API/V1/Posts/` the author is indicated by the user, "
            "on behalf of which a request is made "
        )

        # post with group
        data = {"text": "Article number 4", "group": group_1.id}
        response = user_api_client.post("/api/v1/posts/", data=data)
        assert response.status_code == 201, (
            "Check that when posting at `/API/V1/Posts/` "
            " You can create an article with a community and returns status 201 "
        )
        assert response.json().get("group") == group_1.id, (
            "Check that when posting at `/API/V1/Posts/` "
            " a publication is created indicating the community "
        )

        test_data = response.json()
        msg_error = "Check that when posting at `/API/V1/Posts/` the dictionary with the data of the new article is returned"
        assert type(test_data) == dict, msg_error
        assert test_data.get("text") == data["text"], msg_error

        assert (
            test_data.get("author") == user.username
        ), "Check that when posting at `/API/V1/Posts/` an article is created from an authorized user "
        assert (
            post_count + 2 == Post.objects.count()
        ), "Check that when posting on `/API/V1/Posts/` Article is created"

    @pytest.mark.django_db(transaction=True)
    def test_post_get_current(self, user_api_client, post, user):
        response = user_api_client.get(f"/api/v1/posts/{post.id}/")

        assert (
            response.status_code == 200
        ), "Page `/API/V1/Posts/{ID}/` Not found, check this address in *urls.py *"

        test_data = response.json()
        assert test_data.get("text") == post.text, (
            "Check that when a GET request is `/API/V1/Posts/{ID}/` Return the data of the serializer, "
            "no or incorrect value of `text` "
        )
        assert test_data.get("author") == user.username, (
            "Check that when a GET request is `/API/V1/Posts/{ID}/` Return the data of the serializer, "
            "no or incorrect value of `author`, must return the user name "
        )

    @pytest.mark.django_db(transaction=True)
    def test_post_patch_current(self, user_api_client, post, another_post):
        response = user_api_client.patch(
            f"/api/v1/posts/{post.id}/", data={"text": "Поменяли текст статьи"}
        )

        assert (
            response.status_code == 200
        ), "Check that with a PATCH request `/API/V1/Posts/{ID}/` REMOVE status 200 "

        test_post = Post.objects.filter(id=post.id).first()

        assert (
            test_post
        ), "Check that with a Patch request `/API/V1/Posts/{ID}/` You have not deleted the article "

        assert (
            test_post.text == "Поменяли текст статьи"
        ), "Check that with a patch request `/API/V1/Posts/{ID}/` You change the article "

        response = user_api_client.patch(
            f"/api/v1/posts/{another_post.id}/", data={"text": "Поменяли текст статьи"}
        )

        assert (
            response.status_code == 403
        ), "Check that with a patch request `/API/V1/Posts/{ID}/` for not your article you return status 403 "

    @pytest.mark.django_db(transaction=True)
    def test_post_delete_current(self, user_api_client, post, another_post):
        response = user_api_client.delete(f"/api/v1/posts/{post.id}/")

        assert (
            response.status_code == 204
        ), "Check that when the Delete request is `/API/V1/Posts/{ID}/` Return Status 204 "

        test_post = Post.objects.filter(id=post.id).first()

        assert (
            not test_post
        ), "Check that when the Delete request is `/API/V1/Posts/{ID}/` You deleted the article "

        response = user_api_client.delete(f"/api/v1/posts/{another_post.id}/")

        assert (
            response.status_code == 403
        ), "Check that when the Delete request is `/API/V1/Posts/{ID}/` for not your article you return the status 403 "
