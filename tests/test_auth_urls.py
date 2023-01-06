import pytest


class TestAuthUrls:
    @pytest.mark.django_db(transaction=True)
    def test_auth_urls(self, client):
        urls = ["/auth/login/", "/auth/logout/", "/auth/signup/"]
        for url in urls:
            try:
                response = client.get(url)
            except Exception as e:
                assert False, f"""Page `{url}` It works incorrectly.Mistake: `{e}`"""
            assert (
                response.status_code != 404
            ), f"Page` Not found, check this address in *urls.py*"
            assert (
                response.status_code == 200
            ), f"Mistake {response.status_code} When opening `{url}`.Check its View function"
