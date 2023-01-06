import pytest
from posts.models import Group


class TestGroupAPI:
    @pytest.mark.django_db(transaction=True)
    def test_group_not_found(self, client, post, group_1):
        response = client.get("/api/v1/groups/")

        assert (
            response.status_code != 404
        ), "Page `/API/V1/Groups/` Not found, check this address in *urls.py *"

    @pytest.mark.django_db(transaction=True)
    def test_group_list_not_auth(self, client, post, group_1):
        response = client.get("/api/v1/groups/")
        assert (
            response.status_code == 200
        ), "Check that `/API/V1/Groups/` when requesting without token, return the status of 200 "

    @pytest.mark.django_db(transaction=True)
    def test_group_single_not_auth(self, client, group_1):
        response = client.get(f"/api/v1/groups/{group_1.id}/")
        assert (
            response.status_code == 200
        ), "Check that `/API/V1/Groups/{Group.id}/` when requesting without token, return the status of 200 "

    @pytest.mark.django_db(transaction=True)
    def test_group_get(self, user_api_client, post, another_post, group_1, group_2):
        response = user_api_client.get("/api/v1/groups/")
        assert (
            response.status_code == 200
        ), "Check that with a GET request `/API/V1/Groups/` with an authorization tokene, status 200 returns"

        test_data = response.json()

        assert (
            type(test_data) == list
        ), "Check that when a GET request on `/API/V1/Groups/` The list is returned "

        assert (
            len(test_data) == Group.objects.count()
        ), "Check that when a GET request on `/API/V1/Groups/` the entire list of groups is returned"

        groups_cnt = Group.objects.count()
        test_group = test_data[0]

        assert (
            "title" in test_group
        ), "Check that they added `Title` to the` Fields` Fields of the Group Model serializer "

        assert (
            len(test_data) == groups_cnt
        ), "Check that when a GET request on `/API/V1/Groups/` the entire list of groups is returned"

    @pytest.mark.django_db(transaction=True)
    def test_group_cannot_create(self, user_api_client, group_1, group_2):
        group_count = Group.objects.count()

        data = {}
        response = user_api_client.post("/api/v1/groups/", data=data)
        assert (
            response.status_code == 405
        ), "Check that when posting on `/API/V1/Groups/` you can not create a community through API "

        data = {"title": "Группа  номер 3"}
        response = user_api_client.post("/api/v1/groups/", data=data)
        assert (
            response.status_code == 405
        ), "Check that when posting on `/API/V1/Groups/` you can not create a community through API "

        assert (
            group_count == Group.objects.count()
        ), "Check that when posting on `/API/V1/Groups/` you can not create a community through API "

    @pytest.mark.django_db(transaction=True)
    def test_group_get(
        self, user_api_client, post, post_2, another_post, group_1, group_2
    ):
        response = user_api_client.get("/api/v1/groups/")
        assert (
            response.status_code == 200
        ), "Page `/API/V1/Groups/` Not found, check this address in *urls.py *"
        test_data = response.json()
        groups_cnt = Group.objects.all().count()
        assert (
            len(test_data) == groups_cnt
        ), "Check that when a GET request on `/API/V1/Groups/` The list of all communities is returned "

        response = user_api_client.get(f"/api/v1/groups/{group_2.id}/")
        assert isinstance(
            response.json(), dict
        ), "When requesting `/API/V1/Groups/{ID}/` a dictionary must be returned "

        g = Group.objects.filter(id=group_2.id)
        json_response = response.json()
        for k in json_response:
            assert k in g.values()[0] and json_response[k] == g.values()[0][k], (
                "Check that when a GET request on `/API/V1/Groups/{ID}/` "
                "Information about the corresponding community is returned"
            )

        response = user_api_client.get(f"/api/v1/groups/{group_1.id}/")
        assert isinstance(
            response.json(), dict
        ), "When requesting `/API/V1/Groups/{ID}/` a dictionary must be returned "
        g = Group.objects.filter(id=group_1.id)
        json_response = response.json()
        for k in json_response:
            assert k in g.values()[0] and json_response[k] == g.values()[0][k], (
                "Check that when a GET request on `/API/V1/Groups/{ID}/` "
                "Information about the corresponding community is returned"
            )
