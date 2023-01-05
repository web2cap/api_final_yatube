from django.db import models


class CreatedModel(models.Model):
    """Abstract model.Adds the date of creation."""

    created = models.DateTimeField(
        "date of creation", auto_now_add=True, db_index=True
    )

    class Meta:
        abstract = True
