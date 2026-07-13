from django.http import JsonResponse
from movies.models import Movie
from recommender.engine import recommend


def recommend_api(request, pk):
    movie = Movie.objects.filter(pk=pk).first()
    if not movie:
        return JsonResponse({"error": "找不到電影"}, status=404)

    results = recommend(pk, top_n=10)
    data = [
        {
            "id": m.id,
            "title": m.title,
            "genre": m.genre,
            "vote_average": m.vote_average,
            "poster_url": m.poster_url(),
            "release_year": m.release_year,
        }
        for m in results
    ]
    return JsonResponse({"recommendations": data})