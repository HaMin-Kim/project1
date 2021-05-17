from django.urls  import path

from movies.views import MovieRankingView, MovieRandomView

urlpatterns= [
	path('/ranking', MovieRankingView.as_view()), 
	path('/random', MovieRandomView.as_view()),
]
