from sklearn.feature_extraction.text import TfidfVectorizer
import json
import os
import django
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

from movies.models import Movie


def build_vectors():
    movies = Movie.objects.all()
    print(f"共 {movies.count()} 部電影要向量化...")

    # 把類型 + 簡介合併成一段文字
    texts = []
    movie_list = list(movies)

    for movie in movie_list:
        genre_text = movie.genre.replace(",", " ")
        combined = f"{genre_text} {movie.overview}".strip()
        texts.append(combined if combined else "unknown")

    # TF-IDF 向量化
    vectorizer = TfidfVectorizer(max_features=500)
    matrix = vectorizer.fit_transform(texts)

    # 存回資料庫
    for i, movie in enumerate(movie_list):
        vector = matrix[i].toarray()[0].tolist()
        movie.vector = vector

    Movie.objects.bulk_update(movie_list, ["vector"])
    print("向量化完成！")


if __name__ == "__main__":
    build_vectors()