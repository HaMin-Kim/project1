from django.urls   import path

from movies.views  import MovieInfoView, Wish

urlpatterns = [
        path('/<int:movie_id>', MovieInfoView.as_view()),
        path('/<int:movie_id>/wish', Wish.as_view())
]