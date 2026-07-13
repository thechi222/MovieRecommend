from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import django
import os
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

from movies.models import Movie


def get_similar_movies(movie_id, top_n=10):
    """
    輸入電影 ID，回傳最相似的 top_n 部電影
    """
    try:
        target = Movie.objects.get(id=movie_id)
    except Movie.DoesNotExist:
        return []

    if not target.vector:
        return []

    all_movies = Movie.objects.exclude(id=movie_id).filter(vector__isnull=False)

    target_vec = np.array(target.vector).reshape(1, -1)
    results = []

    for movie in all_movies:
        movie_vec = np.array(movie.vector).reshape(1, -1)
        score = cosine_similarity(target_vec, movie_vec)[0][0]
        results.append((score, movie))

    # 依相似度排序，取前 top_n
    results.sort(key=lambda x: x[0], reverse=True)
    return [movie for score, movie in results[:top_n]]