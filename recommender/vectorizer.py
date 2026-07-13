import os
import django
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

from movies.models import Movie
from sentence_transformers import SentenceTransformer


def build_vectors():
    print("載入 Sentence-BERT 模型")
    model = SentenceTransformer("paraphrase-multilingual-MiniLM-L12-v2")
    # 選這個模型的原因：支援中文、英文混合，體積適中，效果好

    movies = list(Movie.objects.all())
    print(f"共 {len(movies)} 部電影要向量化...")

    # 把類型 + 簡介合併成一段文字
    texts = []
    for movie in movies:
        genre_text = movie.genre.replace(",", " ")
        combined = f"{genre_text} {movie.overview}".strip()
        texts.append(combined if combined else "未知電影")

    # Sentence-BERT 批次向量化
    print("開始向量化")
    vectors = model.encode(texts, batch_size=32, show_progress_bar=True)

    # 存回資料庫
    print("儲存向量到資料庫...")
    for i, movie in enumerate(movies):
        movie.vector = vectors[i].tolist()

    Movie.objects.bulk_update(movies, ["vector"])
    print(f"完成！共更新 {len(movies)} 部電影的向量")


if __name__ == "__main__":
    build_vectors()