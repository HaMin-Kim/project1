from django.urls   import path

from movies.views  import MovieInfoView

urlpatterns = [
        path('/info/<int:movie_id>', MovieInfoView.as_view()),
]
