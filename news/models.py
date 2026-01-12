from django.conf import settings
from django.db import models
from django.utils import timezone


class Category(models.Model):
    name = models.CharField(max_length=120, unique=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class News(models.Model):
    title = models.CharField(max_length=200)
    text = models.TextField()
    image = models.ImageField(upload_to="news/", blank=True, null=True)
    categories = models.ManyToManyField(Category, related_name="news", blank=True)
    created_at = models.DateTimeField(default=timezone.now, db_index=True)

    favorites = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        through="NewsFavorite",
        related_name="favorite_news",
        blank=True,
    )

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.title


class NewsFavorite(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    news = models.ForeignKey(News, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)

    class Meta:
        unique_together = [("user", "news")]
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.user} -> {self.news}"
