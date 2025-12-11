from typing import Any

from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.urls import reverse
from faker.utils.text import slugify


class Book(models.Model):
    title = models.CharField(max_length=50)
    rating = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    author = models.CharField(null=True, max_length=100)
    is_bestselling = models.BooleanField(default=False)
    slug = models.SlugField(default="", null=False, db_index=True)

    def get_absolute_url(self) -> str:
        return reverse("book_detail", args=[self.slug])

    def save(self, *args: Any, **kwargs: Any) -> None:
        self.slug = slugify(self.title)
        super().save()

    def __str__(self) -> str:
        return f"{self.title} ({self.rating})"
