import pytest
from django.contrib.auth import get_user_model

User = get_user_model()

# user_api_client
class TestJWT:
    url_create = "/api/v1/jwt/create/"
    url_refresh = "/api/v1/jwt/refresh/"
    url_verify = "/api/v1/jwt/verify/"

    @pytest.mark.django_db(transaction=True)
    def test_jwt_create__invalid_request_data(self, client, user):
        url = self.url_create
        response = client.post(url)
        code_expected = 400
        assert response.status_code == code_expected, (
            f"Make sure that when requesting `{url}` without parameters, "
            f"Code is returned {code_expected} "
        )
        fields_invalid = ["username", "password"]
        for field in fields_invalid:
            assert field in response.json().keys(), (
                f"Make sure that when requesting `{url}` without parameters, "
                f"Code is returned {code_expected} with a message about "
                " "
                "When processing which fields an error arose. "
                f"No field {field} "
            )

        username_invalid = "invalid_username_not_exists"
        password_invalid = "invalid pwd"
        data_invalid = {"username": username_invalid, "password": password_invalid}
        response = client.post(url, data=data_invalid)
        code_expected = 401
        assert response.status_code == code_expected, (
            f"Make sure that when requesting `{url}` without parameters, "
            f"Code is returned {code_expected} "
        )
        field = "detail"
        assert field in response.json(), (
            f"Make sure that when requesting `{url}` with incorrect username, "
            f"Code is returned {code_expected} with the corresponding message "
            f"In a field {field} "
        )
        username_valid = user.username
        data_invalid = {"username": username_valid, "password": password_invalid}
        response = client.post(url, data=data_invalid)
        assert response.status_code == code_expected, (
            f"Make sure that when requesting `{url}` without parameters, "
            f"Code is returned {code_expected} "
        )
        field = "detail"
        assert field in response.json(), (
            f"Make sure that when requesting `{url}` with incorrect password, "
            f"Code is returned {code_expected} with the corresponding message "
            f"In a field {field} "
        )

    @pytest.mark.django_db(transaction=True)
    def test_jwt_create__valid_request_data(self, client, user):
        url = self.url_create
        valid_data = {"username": user.username, "password": "1234567"}
        response = client.post(url, data=valid_data)
        code_expected = 200
        assert response.status_code == code_expected, (
            f"Make sure that when requesting `{url}` with valid data, "
            f"Code is returned {code_expected} "
        )
        fields_in_response = ["refresh", "access"]
        for field in fields_in_response:
            assert field in response.json().keys(), (
                f"Make sure that when requesting `{url}` with valid data, "
                f" The code is returned {code_expected} with keys"
                f"{fields_in_response}, where tokens are contained "
            )

    @pytest.mark.django_db(transaction=True)
    def test_jwt_refresh__invalid_request_data(self, client):
        url = self.url_refresh

        response = client.post(url)
        code_expected = 400
        assert response.status_code == code_expected, (
            f"Make sure that when requesting `{url}` without parameters, "
            f"Code is returned {code_expected} "
        )
        data_invalid = {"refresh": "invalid token"}
        response = client.post(url, data=data_invalid)
        code_expected = 401
        assert response.status_code == code_expected, (
            f"Make sure that when requesting `{url}` with a non -vibrant value of the Refresh parameter, "
            f"Code is returned {code_expected} "
        )
        fields_expected = ["detail", "code"]
        for field in fields_expected:
            assert field in response.json(), (
                f"Make sure that when requesting `{url}` with a non -vibrant value of the Refresh parameter, "
                f"Code is returned {code_expected} with the corresponding message "
                f"In a field {field} "
            )

    @pytest.mark.django_db(transaction=True)
    def test_jwt_refresh__valid_request_data(self, client, user):
        url = self.url_refresh
        valid_data = {"username": user.username, "password": "1234567"}
        response = client.post(self.url_create, data=valid_data)
        token_refresh = response.json().get("refresh")
        code_expected = 200
        response = client.post(url, data={"refresh": token_refresh})
        assert response.status_code == code_expected, (
            f"Make sure that when requesting `{url}` with a valid parameter Refresh, "
            f"Code is returned {code_expected} "
        )
        field = "access"
        assert field in response.json(), (
            f"Make sure that when requesting `{url}` with a valid parameter Refresh, "
            f"Code is returned {code_expected} and the Access parameter, in which the new token is transferred"
        )

    @pytest.mark.django_db(transaction=True)
    def test_jwt_verify__invalid_request_data(self, client):
        url = self.url_verify

        response = client.post(url)
        code_expected = 400
        assert response.status_code == code_expected, (
            f"Make sure that when requesting `{url}` without parameters, "
            f"Code is returned {code_expected} "
        )
        data_invalid = {"token": "invalid token"}
        response = client.post(url, data=data_invalid)
        code_expected = 401
        assert response.status_code == code_expected, (
            f"Make sure that when requesting `{url}` with the unylic value of the token parameter, "
            f"Code is returned {code_expected} "
        )
        fields_expected = ["detail", "code"]
        for field in fields_expected:
            assert field in response.json(), (
                f"Make sure that when requesting `{url}` with the unylic value of the token parameter, "
                f"Code is returned {code_expected} with the corresponding message "
                f"In a field {field} "
            )

    @pytest.mark.django_db(transaction=True)
    def test_jwt_verify__valid_request_data(self, client, user):
        url = self.url_verify
        valid_data = {"username": user.username, "password": "1234567"}
        response = client.post(self.url_create, data=valid_data)
        token_access = response.json().get("access")
        token_refresh = response.json().get("refresh")
        code_expected = 200
        response = client.post(url, data={"token": token_access})
        assert response.status_code == code_expected, (
            f"Make sure that when requesting `{url}` with a valid Token parameter, "
            f"Code is returned {code_expected}."
            "Validation should undergo both Refresh and Access tokens"
        )
        response = client.post(url, data={"token": token_refresh})
        assert response.status_code == code_expected, (
            f"Make sure that when requesting `{url}` with a valid Token parameter, "
            f"Code is returned {code_expected}."
            "Validation should undergo both Refresh and Access tokens"
        )
