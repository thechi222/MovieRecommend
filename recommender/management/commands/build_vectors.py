from django.core.management.base import BaseCommand
from recommender.vectorizer import build_vectors


class Command(BaseCommand):
    help = "把所有電影簡介轉成 TF-IDF 向量存入資料庫"

    def handle(self, *args, **kwargs):
        self.stdout.write("開始向量化...")
        build_vectors()
        self.stdout.write(self.style.SUCCESS("向量化完成！"))