from django.db import models


class Movie(models.Model):
    # 基本資訊
    tmdb_id = models.IntegerField(unique=True)
    title = models.CharField(max_length=255)
    original_title = models.CharField(max_length=255, blank=True)
    overview = models.TextField(blank=True)
    release_date = models.DateField(null=True, blank=True)
    release_year = models.IntegerField(null=True, blank=True)

    # 評分
    vote_average = models.FloatField(default=0)
    vote_count = models.IntegerField(default=0)
    popularity = models.FloatField(default=0)

    # 類型（存成逗號分隔字串，例如 "動作,冒險,科幻"）
    genre = models.CharField(max_length=255, blank=True)

    # 圖片
    poster_path = models.CharField(max_length=255, blank=True)
    backdrop_path = models.CharField(max_length=255, blank=True)

    # 語言
    original_language = models.CharField(max_length=10, blank=True)

    # 推薦引擎用（之後向量化會用到）
    vector = models.JSONField(null=True, blank=True)

    # 資料來源標記
    source = models.CharField(
        max_length=20,
        choices=[('popular', '熱門'), ('top_rated', '高分')],
        default='top_rated'
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-vote_average']

    def __str__(self):
        return f"{self.title} ({self.release_year})"

    def poster_url(self):
        if self.poster_path:
            return f"https://image.tmdb.org/t/p/w500{self.poster_path}"
        return ""