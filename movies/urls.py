from django.urls import path

from movies.views import MainPageView

urlpatterns= [
	path('/movies', MainPageView.as_view()),
]
