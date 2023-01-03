import re
import tempfile

import pytest
from django.contrib.admin.sites import site
from django.contrib.auth import get_user_model
from django.db.models import fields
from django.template.loader import select_template
from django.core.paginator import Page

from tests.utils import get_field_from_context

try:
    from posts.models import Post
except ImportError:
    assert False, 'No model was found Post'

try:
    from posts.models import Group
except ImportError:
    assert False, 'No model was found Group'


def search_field(fields, attname):
    for field in fields:
        if attname == field.attname:
            return field
    return None


def search_refind(execution, user_code):
    """Search for launch"""
    for temp_line in user_code.split('\n'):
        if re.search(execution, temp_line):
            return True
    return False


class TestPost:

    def test_post_model(self):
        model_fields = Post._meta.fields
        text_field = search_field(model_fields, 'text')
        assert text_field is not None, 'Add the name of the event `text` model` post`'
        assert type(text_field) == fields.TextField, (
            'Property `Text` Models` Post` should be textual `Textfield`'
        )

        pub_date_field_name = 'created'
        pub_date_field = search_field(model_fields, 'pub_date')
        if pub_date_field is not None:
            pub_date_field_name = 'pub_date'
        else:
            pub_date_field = search_field(model_fields, 'created')
            if pub_date_field is not None:
                pub_date_field_name = 'created'

        assert pub_date_field is not None, (
            f'Add the date and time of the event in `{pub_date_field_name}` patterns `Post`'
        )
        assert type(pub_date_field) == fields.DateTimeField, (
            f'Property `{pub_date_field_name}` Models `post` should be a date and time `DateTimeField`'
        )
        assert pub_date_field.auto_now_add, (
            f'Property `pub_date` or `created` - `Post` It must be `auto_now_add`'
        )

        author_field = search_field(model_fields, 'author_id')
        assert author_field is not None, 'Add a user, the author who created the event `Author` Model` Post`'
        assert type(author_field) == fields.related.ForeignKey, (
            'Property `author` Models `Post` should be a link to another model` Foreignkey`'
        )
        assert author_field.related_model == get_user_model(), (
            'Property `author` Models `Post` should be a link to the users model` user`'
        )

        group_field = search_field(model_fields, 'group_id')
        assert group_field is not None, 'Add the `Group` property to the` post` model'
        assert type(group_field) == fields.related.ForeignKey, (
            'Property `group`Models `Post` should be a link to another model` Foreignkey`'
        )
        assert group_field.related_model == Group, (
            'Property `group` Models `Post` should be a link to the` Group` model'
        )
        assert group_field.blank, (
            'Property `group` Models `Post` should be with the attribute` Blank = True`'
        )
        assert group_field.null, (
            'Property `group` Models `post` should be with the attribute` null = true`'
        )

        image_field = search_field(model_fields, 'image')
        assert image_field is not None, 'Add the `iMage` property to the` post` model'
        assert type(image_field) == fields.files.ImageField, (
            'Property `image` Models `Post` should be` Imagefield`'
        )
        assert image_field.upload_to == 'posts/', (
            "Property `image` Models `Post` should be with the attribute` upload_to = 'Posts/' `"
        )

    @pytest.mark.django_db(transaction=True)
    def test_post_create(self, user):
        text = 'Test post'
        author = user

        assert Post.objects.count() == 0

        image = tempfile.NamedTemporaryFile(suffix=".jpg").name
        post = Post.objects.create(text=text, author=author, image=image)
        assert Post.objects.count() == 1
        assert Post.objects.get(text=text, author=author).pk == post.pk

    def test_post_admin(self):
        admin_site = site

        assert Post in admin_site._registry, 'Register `Post` in the admin panel '

        admin_model = admin_site._registry[Post]

        assert 'text' in admin_model.list_display, (
            'Add `text` to display in the list of a model of an administrative site '
        )

        assert 'pub_date' in admin_model.list_display or 'created' in admin_model.list_display, (
            f'Add `Pub_Date` or` CREATED` to display in the list of a model of an administrative site '
        )
        assert 'author' in admin_model.list_display, (
            'Add `author` to display in the list of a model of an administrative site '
        )

        assert 'text' in admin_model.search_fields, (
            'Add `text` to search for a model of an administrative site '
        )

        assert 'pub_date' in admin_model.list_filter or 'created' in admin_model.list_filter, (
            f'Add `Pub_Date` or` CREATED` to filter the administrative site model '
        )

        assert hasattr(admin_model, 'empty_value_display'), (
            'Add the default value `-empty-` for an empty field '
        )
        assert admin_model.empty_value_display == '-empty-', (
            'Add the default value `-empty-` for an empty field '
        )


class TestGroup:

    def test_group_model(self):
        model_fields = Group._meta.fields
        title_field = search_field(model_fields, 'title')
        assert title_field is not None, 'Add the name of the event `Title` Model` Group` '
        assert type(title_field) == fields.CharField, (
            'Property `title` Models `Group` should be sympathetic` charfield` '
        )
        assert title_field.max_length == 200, 'Ask the maximum length of the `title` model` Group` 200 '

        slug_field = search_field(model_fields, 'slug')
        assert slug_field is not None, 'Add the unique address of the `Slug` model` Group` '
        assert type(slug_field) == fields.SlugField, (
            'Property `slug` Models `Group` should be` slugfield` '
        )
        assert slug_field.unique, 'Property `slug` Models `Group` should be unique '

        description_field = search_field(model_fields, 'description')
        assert description_field is not None, 'Add a description of `description` Model` Group` '
        assert type(description_field) == fields.TextField, (
            'Property `description` Models `Group` should be textual` TextField` '
        )

    @pytest.mark.django_db(transaction=True)
    def test_group_create(self, user):
        text = 'Test post'
        author = user

        assert Post.objects.count() == 0

        post = Post.objects.create(text=text, author=author)
        assert Post.objects.count() == 1
        assert Post.objects.get(text=text, author=author).pk == post.pk

        title = 'Test group'
        slug = 'test-link'
        description = 'Test description of the group'

        assert Group.objects.count() == 0
        group = Group.objects.create(title=title, slug=slug, description=description)
        assert Group.objects.count() == 1
        assert Group.objects.get(slug=slug).pk == group.pk

        post.group = group
        post.save()
        assert Post.objects.get(text=text, author=author).group == group


class TestGroupView:

    @pytest.mark.django_db(transaction=True)
    def test_group_view(self, client, post_with_group):
        url = f'/group/{post_with_group.group.slug}'
        url_templ = '/group/<slug>/'
        try:
            response = client.get(url)
        except Exception as e:
            assert False, f'''Page `{url_templ}` It works incorrectly.Mistake: `{e}`'''
        if response.status_code in (301, 302):
            response = client.get(f'{url}/')
        if response.status_code == 404:
            assert False, f'Page `{url_templ}` Not found, check this address in *urls.py*'

        if response.status_code != 200:
            assert False, f'Page `{url_templ}` It works incorrectly.'

        page_context = get_field_from_context(response.context, Page)
        assert page_context is not None, (
            f'Check what you transferred to the author’s articles to the context of the page `{url_templ}` type `Page`'
        )
        assert len(page_context.object_list) == 1, (
            f'Check that the author’s correct articles are transferred to the context of the page `{url_templ}`'
        )
        posts_list = page_context.object_list
        for post in posts_list:
            assert hasattr(post, 'image'), (
                f'Make sure the article transmitted to the context of the page `{url_templ}`, It has a field `Image`'
            )
            assert getattr(post, 'image') is not None, (
                f'Make sure the article transmitted to the context of the page `{url_templ}`, It has a field `Image` ' 
                'And the image is transmitted there'
            )

        group = post_with_group.group
        html = response.content.decode()

        templates_list = ['group_list.html', 'posts/group_list.html']
        html_template = select_template(templates_list).template.source

        assert search_refind(r'{%\s*for\s+.+in.*%}', html_template), (
            'Edit the HTML-header, use the cycle tag'
        )
        assert search_refind(r'{%\s*endfor\s*%}', html_template), (
            'Edit the HTML-header, the closing tag of the cycle has not been found'
        )

        assert re.search(
            group.title,
            html
        ), (
            'Edit the HTML-header, the title of the group '
            '`{% block header %}{{ The name of the_group }}{% endblock %}`'
        )
        assert re.search(
            r'<\s*p\s*>\s*' + group.description + r'\s*<\s*\/p\s*>',
            html
        ), 'Edit the HTML-shaped, no description of the group `<p>{{ Description of the_group }}</p>`'


class TestCustomErrorPages:

    @pytest.mark.django_db(transaction=True)
    def test_custom_404(self, client):
        url_invalid = '/some_invalid_url_404/'
        code = 404
        response = client.get(url_invalid)

        assert response.status_code == code, (
            f'Make sure that for non -existent page addresses, the server returns the code {code}'
        )

        try:
            from yatube.urls import handler404 as handler404_student
        except ImportError:
            assert False, (
                f'Make sure for pages returning the code {code}, '
                'The custom template is configured'
            )

    @pytest.mark.django_db(transaction=True)
    def test_custom_500(self):
        code = 500

        try:
            from yatube.urls import handler500
        except ImportError:
            assert False, (
                f'Make sure for pages returning the code {code}, '
                'The custom template is configured'
            )

    @pytest.mark.django_db(transaction=True)
    def test_custom_403(self):
        code = 403

        try:
            from yatube.urls import handler403
        except ImportError:
            assert False, (
                f'Make sure for pages returning the code {code}, '
                'The custom template is configured'
            )
