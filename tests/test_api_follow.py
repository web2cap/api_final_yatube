import pytest

from posts.models import Follow


class TestFollowAPI:

    @pytest.mark.django_db(transaction=True)
    def test_follow_not_found(self, client, follow_1, follow_2):
        response = client.get('/api/v1/follow/')

        assert response.status_code != 404, (
            'Page `/API/V1/Follow/` Not found, check this address in *urls.py *'
        )
        assert response.status_code != 500, (
            'Page `/API/V1/Follow/` cannot be treated with your server, check the View function in *views.PY *'
        )

    @pytest.mark.django_db(transaction=True)
    def test_follow_not_auth(self, client, follow_1, follow_2):
        response = client.get('/api/v1/follow/')
        assert response.status_code == 401, (
            'Check that `/API/V1/Follow/` during GET request without token returns the status of 401 '
        )

        data = {}
        response = client.post('/api/v1/follow/', data=data)
        assert response.status_code == 401, (
            'Check that `/API/V1/Follow/` when post without token returns status 401 '
        )

    @pytest.mark.django_db(transaction=True)
    def test_follow_get(self, user_api_client, user, follow_1, follow_2, follow_3):
        response = user_api_client.get('/api/v1/follow/')
        assert response.status_code == 200, (
            'Check that when a GET request is `/API/V1/Follow/` with an authorization token status 200 returns'
        )

        test_data = response.json()

        assert type(test_data) == list, (
            'Check that when a GET request on `/API/V1/Follow/` Returns the list '
        )

        assert len(test_data) == Follow.objects.filter(following__username=user.username).count(), (
            'Check that when a GET request on `/API/V1/Follow/` is the list of all user subscribers is returned'
        )

        follow = Follow.objects.filter(user=user)[0]
        test_group = test_data[0]
        assert 'user' in test_group, (
            'Check that they added `user` to the` Fields` field of the Follow model serializer '
        )
        assert 'following' in test_group, (
            'Check that you added `following` to the` Fields` field of the Follow model serializer '
        )

        assert test_group['user'] == follow.user.username, (
            'Check that when a GET request on `/API/V1/Follow/` is the list of subscriptions of the current user is returned, '
            'In the field `user` should be` username` '
        )
        assert test_group['following'] == follow.following.username, (
            'Check that when a GET request on `/API/V1/Follow/` the entire list of subscriptions is returned, '
            'In the field `following` should be` username` '
        )

    @pytest.mark.django_db(transaction=True)
    def test_follow_create(self, user_api_client, follow_2, follow_3, user, user_2, another_user):
        follow_count = Follow.objects.count()

        data = {}
        response = user_api_client.post('/api/v1/follow/', data=data)
        assert response.status_code == 400, (
            'Check that when posting at `/API/V1/Follow/` Status 400 is returned with incorrect data'
        )

        data = {'following': another_user.username}
        response = user_api_client.post('/api/v1/follow/', data=data)
        assert response.status_code == 201, (
            'Check that when posting at `/API/V1/Follow/` Status 201 returns the correct data with the correct data'
        )

        test_data = response.json()

        msg_error = (
            'Check that when posting at `/API/V1/Follow/` the dictionary with the data of the new subscription is returned'
        )
        assert type(test_data) == dict, msg_error
        assert test_data.get('user') == user.username, msg_error
        assert test_data.get('following') == data['following'], msg_error

        assert follow_count + 1 == Follow.objects.count(), (
            'Check that when posting at `/API/V1/Follow/` Subscription is created '
        )

        response = user_api_client.post('/api/v1/follow/', data=data)
        assert response.status_code == 400, (
            'Check that when posting at `/API/V1/Follow/` '
            'The status of 400 is returned to the already signed author'
        )

        data = {'following': user.username}
        response = user_api_client.post('/api/v1/follow/', data=data)
        assert response.status_code == 400, (
            'Check that when posting at `/API/V1/Follow/` '
            'When trying to subscribe to himself, status 400 returns'
        )

    @pytest.mark.django_db(transaction=True)
    def test_follow_search_filter(self, user_api_client, follow_1, follow_2,
                                  follow_3, follow_4, follow_5,
                                  user, user_2, another_user):

        follow_user = Follow.objects.filter(user=user)
        follow_user_cnt = follow_user.count()

        response = user_api_client.get('/api/v1/follow/')
        assert response.status_code != 404, (
            'Page `/API/V1/Follow/` Not found, check this address in *urls.py *'
        )
        assert response.status_code == 200, (
            'Page `/API/V1/Follow/` does not work, check the View Function '
        )

        test_data = response.json()
        assert len(test_data) == follow_user_cnt, (
            'Check that when a GET request on `/API/V1/Follow/` is the list of all user subscriptions is returned'
        )

        response = user_api_client.get(f'/api/v1/follow/?search={user_2.username}')
        assert len(response.json()) == follow_user.filter(following=user_2).count(), (
            'Check that when a GET request with the `Search` parameter on`/API/V1/Follow/`'
            'The result of the subscription search is returned'
        )

        response = user_api_client.get(f'/api/v1/follow/?search={another_user.username}')
        assert len(response.json()) == follow_user.filter(following=another_user).count(), (
            'Check that when a GET request with the `Search` parameter on`/API/V1/Follow/`'
            'The result of the subscription search is returned'
        )
