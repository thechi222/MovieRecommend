from django.db import models
from django.contrib.auth.models import User
from movies.models import Movie


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    favorite_genres = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} 的個人檔案"


class Watchlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="watchlist")
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name="watchlisted_by")
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("user", "movie")
        ordering = ["-added_at"]

    def __str__(self):
        return f"{self.user.username} 收藏了 {self.movie.title}"


class WatchHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="watch_history")
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name="watched_by")
    watched_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-watched_at"]

    def __str__(self):
        return f"{self.user.username} 看過 {self.movie.title}"