from django.contrib.auth import get_user_model
from django.db import models
from core.models import CreatedModel

User = get_user_model()


class Group(models.Model):
    title = models.CharField(
        max_length=200,
        verbose_name="Name",
        help_text="Enter the name of the group",
    )
    slug = models.SlugField(
        unique=True,
        verbose_name="Link to the group",
        help_text="Indicate the link to the group",
    )
    description = models.TextField(
        verbose_name="Description",
        help_text="Enter the description of the group"
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )
    
    class Meta:
        verbose_name = "Group"
        verbose_name_plural = "Groups"

    def __str__(self) -> str:
        return self.title


class Post(CreatedModel):
    text = models.TextField(
        verbose_name="Text records", help_text="Enter the text of the post"
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="posts",
        verbose_name="The author of the publication",
    )
    group = models.ForeignKey(
        Group,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="posts",
        verbose_name="Group",
        help_text="Choose a group",
    )
    image = models.ImageField(
        "Picture",
        upload_to="posts/",
        blank=True,
        null=True
    )

    class Meta:
        ordering = ("-pub_date",)
        verbose_name = "Post"
        verbose_name_plural = "Posts"

    def __str__(self) -> str:
        return self.text[:15]


class Comment(models.Model):
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name="comments",
        verbose_name="Post",
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="comments",
        verbose_name="The author of the commentary",
    )
    text = models.TextField(
        verbose_name="The text of the comment",
        help_text="Enter the text of the comment",
    )
    created = models.DateTimeField(
        "date of creation", auto_now_add=True, db_index=True
    )

    class Meta:
        ordering = ("-created",)
        verbose_name = "Comment"
        verbose_name_plural = "Comments"

    def __str__(self) -> str:
        return self.text[:15]


class Follow(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="follower",
        verbose_name="Follower",
    )
    following = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="following_author",
        verbose_name="Author",
    )

    class Meta:
        verbose_name = "Subscription"
        verbose_name_plural = "Subscriptions"
        constraints = [
            models.UniqueConstraint(
                fields=["user", "following"], name="unique_follow"
            )
        ]

    def __str__(self) -> str:
        return f"{self.user.username} on {self.author.username}"
