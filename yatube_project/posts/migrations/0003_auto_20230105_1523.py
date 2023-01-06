import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("posts", "0002_group_author"),
    ]

    operations = [
        migrations.RemoveConstraint(model_name="follow", name="unique_follow",),
        migrations.RemoveField(model_name="follow", name="author",),
        migrations.AddField(
            model_name="follow",
            name="following",
            field=models.ForeignKey(
                default=None,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="following_author",
                to="auth.user",
                verbose_name="Author",
            ),
            preserve_default=False,
        ),
        migrations.AddConstraint(
            model_name="follow",
            constraint=models.UniqueConstraint(
                fields=("user", "following"), name="unique_follow"
            ),
        ),
    ]
