import pytest


class TestTemplateView:

    @pytest.mark.django_db(transaction=True)
    def test_about_author_tech(self, client):
        urls = ['/about/author/', '/about/tech/']
        for url in urls:
            try:
                response = client.get(url)
            except Exception as e:
                assert False, f'''Page `{url}` It works incorrectly.Mistake: `{e}`'''
            assert response.status_code != 404, f'Page `{url}` Not found, check this address in *urls.py*'
            assert response.status_code == 200, (
                f'Mistake {response.status_code} When opening `{url}`.Check its View function'
            )
