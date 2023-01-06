import tempfile

import pytest
from mixer.backend.django import mixer as _mixer
from posts.models import Comment, Follow, Group, Post


@pytest.fixture()
def mock_media(settings):
    with tempfile.TemporaryDirectory() as temp_directory:
        settings.MEDIA_ROOT = temp_directory
        yield temp_directory


@pytest.fixture
def mixer():
    return _mixer


@pytest.fixture
def group_1():
    return Group.objects.create(title="Group 1", slug="group_1")


@pytest.fixture
def group_2():
    return Group.objects.create(title="Group 2", slug="group_2")


@pytest.fixture
def post(user, group_1):
    image = tempfile.NamedTemporaryFile(suffix=".jpg").name
    return Post.objects.create(
        text="Test post 1", author=user, image=image, group=group_1
    )


@pytest.fixture
def post_2(user, group_1):
    return Post.objects.create(text="Test post 12342341", author=user, group=group_1)


@pytest.fixture
def group():
    return Group.objects.create(
        title="Test group 1",
        slug="test-link",
        description="Test description of the group",
    )


@pytest.fixture
def post_with_group(user, group):
    image = tempfile.NamedTemporaryFile(suffix=".jpg").name
    return Post.objects.create(
        text="Test post 2", author=user, group=group, image=image
    )


@pytest.fixture
def few_posts_with_group(mixer, user, group):
    """Return one record with the same author and group."""
    posts = mixer.cycle(20).blend(Post, author=user, group=group)
    return posts[0]


@pytest.fixture
def another_few_posts_with_group_with_follower(mixer, user, another_user, group):
    mixer.blend("posts.Follow", user=user, author=another_user)
    mixer.cycle(20).blend(Post, author=another_user, group=group)


@pytest.fixture
def comment_1_post(post, user):
    return Comment.objects.create(author=user, post=post, text="Comment 1")


@pytest.fixture
def comment_2_post(post, another_user):
    return Comment.objects.create(author=another_user, post=post, text="Comment 2")


@pytest.fixture
def another_post(another_user, group_2):
    return Post.objects.create(text="Test post 2", author=another_user, group=group_2)


@pytest.fixture
def comment_1_another_post(another_post, user):
    return Comment.objects.create(author=user, post=another_post, text="Comment 12")


@pytest.fixture
def follow_1(user, another_user):
    return Follow.objects.create(user=user, following=another_user)


@pytest.fixture
def follow_2(user_2, user):
    return Follow.objects.create(user=user_2, following=user)


@pytest.fixture
def follow_3(user_2, another_user):
    return Follow.objects.create(user=user_2, following=another_user)


@pytest.fixture
def follow_4(another_user, user):
    return Follow.objects.create(user=another_user, following=user)


@pytest.fixture
def follow_5(user_2, user):
    return Follow.objects.create(user=user, following=user_2)
