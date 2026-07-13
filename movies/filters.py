import django_filters
from movies.models import Movie


class MovieFilter(django_filters.FilterSet):
    title = django_filters.CharFilter(lookup_expr="icontains", label="片名")
    genre = django_filters.CharFilter(lookup_expr="icontains", label="類型")
    release_year = django_filters.NumberFilter(label="年份")
    release_year_gte = django_filters.NumberFilter(field_name="release_year", lookup_expr="gte", label="年份從")
    release_year_lte = django_filters.NumberFilter(field_name="release_year", lookup_expr="lte", label="年份到")
    vote_average_gte = django_filters.NumberFilter(field_name="vote_average", lookup_expr="gte", label="最低評分")
    vote_average_lte = django_filters.NumberFilter(field_name="vote_average", lookup_expr="lte", label="最高評分")

    class Meta:
        model = Movie
        fields = ["title", "genre", "release_year", "vote_average"]