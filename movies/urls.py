from django.urls   import path

from movies.views  import MovieCommentView

urlpatterns = [
	path('/info/<int:movie_id>/comment', MovieCommentView.as_view()),
	path('/info/<int:movie_id>/comment/<int:comment_id>', MovieCommentView.as_view()),
]
