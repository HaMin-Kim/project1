from django.urls  import path

from movies.views import MovieInfoView

urlpatterns= [
	path('/movies', MovieInfoView.as_view()), 
]
