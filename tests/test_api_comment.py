import pytest

from posts.models import Comment


class TestCommentAPI:

    @pytest.mark.django_db(transaction=True)
    def test_comments_not_authenticated(self, client, post):
        response = client.get(f'/api/v1/posts/{post.id}/comments/')

        code = 200
        assert response.status_code == code, (
            'Anonymous user when requesting `/API/V1/Posts/{post.id}/comments/` '
            f'should receive an answer with the code {code} '
        )

    @pytest.mark.django_db(transaction=True)
    def test_comment_single_not_authenticated(self, client, post, comment_1_post):
        response = client.get(f'/api/v1/posts/{post.id}/comments/{comment_1_post.id}/')

        code = 200
        assert response.status_code == code, (
            'Anonymous user when requesting `/API/V1/Posts/{post.id}/comments/{comment.id}` '
            f'should receive an answer with the code {code} '
        )

    @pytest.mark.django_db(transaction=True)
    def test_comments_not_found(self, user_api_client, post):
        response = user_api_client.get(f'/api/v1/posts/{post.id}/comments/')

        assert response.status_code != 404, (
            'Page `/API/V1/Posts/{Post.id}/comments/` Not found, check this address in *urls.py *'
        )

    @pytest.mark.django_db(transaction=True)
    def test_comments_get(self, user_api_client, post, comment_1_post, comment_2_post, comment_1_another_post):
        response = user_api_client.get(f'/api/v1/posts/{post.id}/comments/')

        assert response.status_code == 200, (
            'Check that when a GET request is `/API/V1/Posts/{post.id}/comments/` '
            'With the authorization token, the status of 200 is returned'
        )
        test_data = response.json()
        assert type(test_data) == list, (
            'Check that when a GET request on `/API/V1/Posts/{post.id}/comments/` Returns the list '
        )
        assert len(test_data) == Comment.objects.filter(post=post).count(), (
            'Check that when a GET request on `/API/V1/Posts/{post.id}/comments/` '
            'The entire list of comments of the article is returned'
        )

        comment = Comment.objects.filter(post=post).first()
        test_comment = test_data[0]
        assert 'id' in test_comment, (
            'Check that they added `ID` to the` Fields` field of the Comment model serializer '
        )
        assert 'text' in test_comment, (
            'Check that they added `Text` to the` Fields` field of the Comment model serializer '
        )
        assert 'author' in test_comment, (
            'Check that they added `Author` to the` Fields` Fields Severizer of the Comment Model'
        )
        assert 'post' in test_comment, (
            'Check that they added `post` to the` fields` field of the Comment model serializer '
        )
        assert 'created' in test_comment, (
            'Check what you added `Created` to the` Fields` Fields Severizer of the Comment Model'
        )
        assert test_comment['author'] == comment.author.username, (
            'Check that the `Author` serializer of the Comment model returns the users name '
        )
        assert test_comment['id'] == comment.id, (
            'Check that when a GET request on `/API/V1/Posts/{post.id}/comments/` the entire list of articles is returned'
        )

    @pytest.mark.django_db(transaction=True)
    def test_comments_create(self, user_api_client, post, user, another_user):
        comments_count = Comment.objects.count()

        data = {}
        response = user_api_client.post(f'/api/v1/posts/{post.id}/comments/', data=data)
        assert response.status_code == 400, (
            'Check that when posting at `/API/V1/Posts/{Post.id}/comments/` '
            'With incorrect data, status 400 returns'
        )

        data = {'author': another_user.id, 'text': 'Новый коммент 1233', 'post': post.id}
        response = user_api_client.post(f'/api/v1/posts/{post.id}/comments/', data=data)
        assert response.status_code == 201, (
            'Check that when posting at `/API/V1/Posts/{Post.id}/comments/` '
            'The status of 201 is returned with the correct data'
        )

        test_data = response.json()
        msg_error = (
            'Check that when posting at `/API/V1/Posts/{Post.id}/comments/` '
            'The dictionary is returned with the data of a new comment '
        )
        assert type(test_data) == dict, msg_error
        assert test_data.get('text') == data['text'], msg_error

        assert test_data.get('author') == user.username, (
            'Check that when posting at `/API/V1/Posts/{Post.id}/comments/` '
            'A comment is created from an authorized user '
        )
        assert comments_count + 1 == Comment.objects.count(), (
            'Check that when posting at `/API/V1/Posts/{Post.id}/comments/` Comment is created '
        )

    @pytest.mark.django_db(transaction=True)
    def test_comment_get_current(self, user_api_client, post, comment_1_post, user):
        response = user_api_client.get(f'/api/v1/posts/{post.id}/comments/{comment_1_post.id}/')

        assert response.status_code == 200, (
            'Page `/API/V1/Posts/{Post.id}/comments/{comment.id}/` Not found, '
            'Check this address in *urls.py *'
        )

        test_data = response.json()
        assert test_data.get('text') == comment_1_post.text, (
            'Check that when a GET request is `/API/V1/Posts/{post.id}/comments/{comment.id}/` '
            'Return the data of the serializer, no or incorrect value of `text` '
        )
        assert test_data.get('author') == user.username, (
            'Check that when a GET request is `/API/V1/Posts/{post.id}/comments/{comment.id}/` '
            'Return the data of the serializer, no or incorrect value of `author`, '
            'must return the user name '
        )
        assert test_data.get('post') == post.id, (
            'Check that when a GET request is `/API/V1/Posts/{post.id}/comments/{comment.id}/` '
            'Return the data of the serializer, no or incorrect value of `post` '
        )

    @pytest.mark.django_db(transaction=True)
    def test_comment_patch_current(self, user_api_client, post, comment_1_post, comment_2_post):
        response = user_api_client.patch(f'/api/v1/posts/{post.id}/comments/{comment_1_post.id}/',
                                     data={'text': 'Changed the text of the comment'})

        assert response.status_code == 200, (
            'Check that with a Patch request `/API/V1/Posts/{Post.id}/comments/{comment.id}/` '
            'Return status 200 '
        )

        test_comment = Comment.objects.filter(id=comment_1_post.id).first()

        assert test_comment, (
            'Check that with a Patch request `/API/V1/Posts/{Post.id}/comments/{comment.id}/` '
            'You have not deleted a comment '
        )

        assert test_comment.text == 'Changed the text of the comment', (
            'Check that with a patch request `/API/V1/Posts/{ID}/` You change the article '
        )

        response = user_api_client.patch(f'/api/v1/posts/{post.id}/comments/{comment_2_post.id}/',
                                     data={'text': 'Changed the text of the article'})

        assert response.status_code == 403, (
            'Check that with a Patch request `/API/V1/Posts/{Post.id}/comments/{comment.id}/` '
            'For not your article, you return the status 403 '
        )

    @pytest.mark.django_db(transaction=True)
    def test_comment_delete_current(self, user_api_client, post, comment_1_post, comment_2_post):
        response = user_api_client.delete(f'/api/v1/posts/{post.id}/comments/{comment_1_post.id}/')

        assert response.status_code == 204, (
            'Check that when the Delete request is `/API/V1/Posts/{post.id}/comments/{comment.id}/` Return status 204 '
        )

        test_comment = Comment.objects.filter(id=post.id).first()

        assert not test_comment, (
            'Check that when the Delete request is `/API/V1/Posts/{post.id}/comments/{comment.id}/` You deleted the comment '
        )

        response = user_api_client.delete(f'/api/v1/posts/{post.id}/comments/{comment_2_post.id}/')

        assert response.status_code == 403, (
            'Check that when the Delete request is `/API/V1/Posts/{post.id}/comments/{comment.id}/` '
            'For not your comment, you return the status 403 '
        )
