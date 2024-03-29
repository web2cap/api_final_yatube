import os
import sys

root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(root_dir)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
root_dir_content = os.listdir(BASE_DIR)
PROJECT_DIR_NAME = "yatube_project"
if PROJECT_DIR_NAME not in root_dir_content or not os.path.isdir(
    os.path.join(BASE_DIR, PROJECT_DIR_NAME)
):
    assert False, (
        f"In the directory`{BASE_DIR}` not found main app dir `{MAIN_APP_NAME}`. "
        f"Make sure you have the right project structure."
    )

MANAGE_PATH = os.path.join(BASE_DIR, PROJECT_DIR_NAME)
project_dir_content = os.listdir(MANAGE_PATH)
FILENAME = "manage.py"

if FILENAME not in project_dir_content:
    assert False, (
        f"In the directory`{BASE_DIR}` not a top file `{FILENAME}`. "
        f"Make sure you have the right project structure."
    )


from django.utils.version import get_version

assert (
    get_version() > "3.0.0" and get_version() < "4.0.0"
), "Please use the Django version 3"

from yatube.settings import INSTALLED_APPS

assert any(
    app in INSTALLED_APPS for app in ["posts.apps.PostsConfig", "posts"]
), "Please register the application in `settings.INSTALLED_APPS`"

pytest_plugins = [
    "tests.fixtures.fixture_user",
    "tests.fixtures.fixture_data",
]
