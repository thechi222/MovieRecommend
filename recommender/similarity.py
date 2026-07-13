import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
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
    用矩陣運算一次算完，比逐一比對快很多
    """
    try:
        target = Movie.objects.get(id=movie_id)
    except Movie.DoesNotExist:
        return []

    if not target.vector:
        return []

    # 一次撈所有有向量的電影（排除自己）
    all_movies = list(Movie.objects.exclude(id=movie_id).filter(vector__isnull=False))
    if not all_movies:
        return []

    # 建立矩陣（一次算完所有相似度，比 for loop 快很多）
    target_vec = np.array(target.vector).reshape(1, -1)
    all_vecs = np.array([m.vector for m in all_movies])

    # 一次計算所有相似度
    scores = cosine_similarity(target_vec, all_vecs)[0]

    # 取前 top_n
    top_indices = np.argsort(scores)[::-1][:top_n]
    return [all_movies[i] for i in top_indices]