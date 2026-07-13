from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from movies.models import Movie
from movies.filters import MovieFilter
from recommender.engine import recommend


def movie_list(request):
    movies = Movie.objects.all().order_by("-vote_average")
    f = MovieFilter(request.GET, queryset=movies)
    filtered = f.qs

    all_genres = set()
    for movie in Movie.objects.all():
        for g in movie.genre.split(","):
            if g.strip():
                all_genres.add(g.strip())
    all_genres = sorted(all_genres)

    paginator = Paginator(filtered, 20)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(request, "movies/list.html", {
        "page_obj": page_obj,
        "filter": f,
        "all_genres": all_genres,
        "total": filtered.count(),
    })


def movie_detail(request, pk):
    movie = get_object_or_404(Movie, pk=pk)
    recommendations = recommend(movie.id, top_n=10)
    genre_list = [g.strip() for g in movie.genre.split(",") if g.strip()]

    # 收藏狀態
    in_watchlist = False
    if request.user.is_authenticated:
        from users.models import Watchlist, WatchHistory
        in_watchlist = Watchlist.objects.filter(
            user=request.user, movie=movie
        ).exists()
        # 自動記錄觀看紀錄
        WatchHistory.objects.create(user=request.user, movie=movie)

    return render(request, "movies/detail.html", {
        "movie": movie,
        "recommendations": recommendations,
        "genre_list": genre_list,
        "in_watchlist": in_watchlist,
    })