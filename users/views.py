from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from users.forms import RegisterForm, LoginForm
from users.models import Watchlist, WatchHistory, UserProfile
from movies.models import Movie
import numpy as np


def register_view(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            UserProfile.objects.create(user=user)
            login(request, user)
            messages.success(request, "註冊成功！歡迎加入 CineMatch")
            return redirect("movies:list")
    else:
        form = RegisterForm()
    return render(request, "users/register.html", {"form": form})


def login_view(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(
                request,
                username=form.cleaned_data["username"],
                password=form.cleaned_data["password"]
            )
            if user:
                login(request, user)
                return redirect(request.GET.get("next", "movies:list"))
            else:
                messages.error(request, "帳號或密碼錯誤")
    else:
        form = LoginForm()
    return render(request, "users/login.html", {"form": form})


def logout_view(request):
    logout(request)
    return redirect("movies:list")


@login_required
def profile_view(request):
    watchlist = Watchlist.objects.filter(user=request.user).select_related("movie")
    history = WatchHistory.objects.filter(user=request.user).select_related("movie").distinct()[:20]

    personal_recs = []
    if watchlist.exists():
        all_vecs = []
        for item in watchlist:
            if item.movie.vector:
                all_vecs.append(item.movie.vector)
        if all_vecs:
            avg_vec = np.mean(all_vecs, axis=0).tolist()
            all_movies = Movie.objects.exclude(
                id__in=watchlist.values_list("movie_id", flat=True)
            ).filter(vector__isnull=False)
            from sklearn.metrics.pairwise import cosine_similarity
            scores = []
            for movie in all_movies:
                score = cosine_similarity([avg_vec], [movie.vector])[0][0]
                scores.append((score, movie))
            scores.sort(key=lambda x: x[0], reverse=True)
            personal_recs = [m for _, m in scores[:10]]

    return render(request, "users/profile.html", {
        "watchlist": watchlist,
        "history": history,
        "personal_recs": personal_recs,
    })


@login_required
@require_POST
def toggle_watchlist(request, pk):
    movie = get_object_or_404(Movie, pk=pk)
    existing = Watchlist.objects.filter(user=request.user, movie=movie)
    if existing.exists():
        existing.delete()
        in_watchlist = False
    else:
        Watchlist.objects.create(user=request.user, movie=movie)
        in_watchlist = True
    return JsonResponse({"in_watchlist": in_watchlist})