import os
import requests
import django
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent.parent))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

from movies.models import Movie

TMDB_API_KEY = os.environ.get("TMDB_API_KEY", "")
BASE_URL = "https://api.themoviedb.org/3"

GENRE_MAP = {
    28: "動作", 12: "冒險", 16: "動畫", 35: "喜劇",
    80: "犯罪", 99: "紀錄片", 18: "劇情", 10751: "家庭",
    14: "奇幻", 36: "歷史", 27: "恐怖", 10402: "音樂",
    9648: "懸疑", 10749: "愛情", 878: "科幻", 10770: "電視電影",
    53: "驚悚", 10752: "戰爭", 37: "西部"
}


def fetch_movies(category="top_rated", pages=10, language="zh-TW"):
    movies = []
    for page in range(1, pages + 1):
        url = f"{BASE_URL}/movie/{category}"
        params = {
            "api_key": TMDB_API_KEY,
            "language": language,
            "page": page
        }
        response = requests.get(url, params=params)
        if response.status_code != 200:
            print(f"第 {page} 頁請求失敗：{response.status_code}")
            continue

        data = response.json()
        movies.extend(data.get("results", []))
        print(f"已抓取 {category} 第 {page} 頁，共 {len(data.get('results', []))} 筆")

    return movies


def fetch_overview_fallback(tmdb_id):
    url = f"{BASE_URL}/movie/{tmdb_id}"
    params = {"api_key": TMDB_API_KEY, "language": "en-US"}
    response = requests.get(url, params=params)
    if response.status_code == 200:
        return response.json().get("overview", "")
    return ""


def save_movies(movies, source="top_rated"):
    saved = 0
    skipped = 0

    for item in movies:
        tmdb_id = item.get("id")
        if not tmdb_id:
            continue

        genre_ids = item.get("genre_ids", [])
        genre_str = ",".join([GENRE_MAP.get(gid, "") for gid in genre_ids if gid in GENRE_MAP])

        overview = (item.get("overview") or "").strip()
        if not overview:
            overview = fetch_overview_fallback(tmdb_id)

        release_date = item.get("release_date") or ""
        release_year = int(release_date[:4]) if release_date and len(release_date) >= 4 else None

        obj, created = Movie.objects.update_or_create(
            tmdb_id=tmdb_id,
            defaults={
                "title": item.get("title") or "",
                "original_title": item.get("original_title") or "",
                "overview": overview,
                "release_date": release_date or None,
                "release_year": release_year,
                "vote_average": item.get("vote_average") or 0,
                "vote_count": item.get("vote_count") or 0,
                "popularity": item.get("popularity") or 0,
                "genre": genre_str,
                "poster_path": item.get("poster_path") or "",
                "backdrop_path": item.get("backdrop_path") or "",
                "original_language": item.get("original_language") or "",
                "source": source,
            }
        )

        if created:
            saved += 1
        else:
            skipped += 1

    print(f"\n完成！新增 {saved} 筆，更新 {skipped} 筆")


def run():
    print("開始抓取 Top Rated 電影（10頁 = 約200筆）...")
    top_rated = fetch_movies("top_rated", pages=10)
    save_movies(top_rated, source="top_rated")

    print("\n開始抓取 Popular 電影（5頁 = 約100筆）...")
    popular = fetch_movies("popular", pages=5)
    save_movies(popular, source="popular")

    print("\n全部完成！")


if __name__ == "__main__":
    run()