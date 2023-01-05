from django import forms
from django.conf import settings

from .models import Comment, Post

POST_MIN_LEN = getattr(settings, "POST_MIN_LEN", None)
COMMENT_MIN_LEN = getattr(settings, "COMMENT_MIN_LEN", None)


class PostForm(forms.ModelForm):
    """The form of adding post."""

    class Meta:
        model = Post
        fields = ["text", "group", "image"]

    def clean_text(self):
        data = self.cleaned_data["text"]

        if len(data) < POST_MIN_LEN:
            raise forms.ValidationError(
                f"The long post should be at least {POST_MIN_LEN} symbols!"
            )

        return data


class CommentForm(forms.ModelForm):
    """The form of adding a comment."""

    class Meta:
        model = Comment
        fields = ["text"]

    def clean_text(self):
        data = self.cleaned_data["text"]

        if len(data) < COMMENT_MIN_LEN:
            raise forms.ValidationError(
                "The length of the comment should be at least"
                f" {COMMENT_MIN_LEN} symbols!"
            )

        return data
