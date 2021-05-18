from django.urls   import path

from movies.views  import MovieCommentView, CommentLikeView

urlpatterns = [
	path('/<int:movie_id>/comment', MovieCommentView.as_view()),
	path('/<int:movie_id>/comment/<int:comment_id>', MovieCommentView.as_view()),
	path('/comment/like', CommentLikeView.as_view()),
]
