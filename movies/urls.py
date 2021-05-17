from django.urls   import path

from movies.views  import MovieInformationView

urlpatterns = [
        path('/<int:movie_id>', MovieInformationView.as_view()),
]
