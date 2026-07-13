from django.core.management.base import BaseCommand
from scraper.spiders.tmdb_spider import run


class Command(BaseCommand):
    help = "從 TMDB 抓取電影資料存入資料庫"

    def handle(self, *args, **kwargs):
        self.stdout.write("開始執行爬蟲...")
        run()
        self.stdout.write(self.style.SUCCESS("爬蟲執行完成！"))