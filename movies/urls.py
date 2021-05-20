from django.urls  import path

from movies.views import MovieMainView

urlpatterns= [
	path('/movies', MovieMainView.as_view()), 
]
