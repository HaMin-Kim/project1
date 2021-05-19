from django.urls   import path

from movies.views  import MovieInfoView, WishMovie

urlpatterns = [
        path('/<int:movie_id>', MovieInfoView.as_view()),
        path('/wishmovie', WishMovie.as_view()),
]
