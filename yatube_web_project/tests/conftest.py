import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
root_dir_content = os.listdir(BASE_DIR)
MAIN_APP_NAME = 'yatube'
if (
        MAIN_APP_NAME not in root_dir_content
        or not os.path.isdir(BASE_DIR)
):
    assert False, (
        f'In the directory`{BASE_DIR}` not found main app dir `{MAIN_APP_NAME}`. '
        f'Make sure you have the right project structure.'
    )

project_dir_content = os.listdir(BASE_DIR)
FILENAME = 'manage.py'
# проверяем, что структура проекта верная, и manage.py на месте
if FILENAME not in project_dir_content:
    assert False, (
        f'In the directory`{BASE_DIR}` not a top file `{FILENAME}`. '
        f'Make sure you have the right project structure.'
    )

from django.utils.version import get_version

assert get_version() > '3.0.0' and  get_version() <'4.0.0', 'Please use the Django version 3'

from yatube.settings import INSTALLED_APPS

assert any(app in INSTALLED_APPS for app in ['posts.apps.PostsConfig', 'posts']), (
    'Please register the application in `settings.INSTALLED_APPS`'
)

pytest_plugins = [
    'tests.fixtures.fixture_user',
    'tests.fixtures.fixture_data',
]
