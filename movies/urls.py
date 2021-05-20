from django.urls   import path

from movies.views  import MovieInfoView, MovieCommentView, CommentLikeView, Rating, Wish

urlpatterns = [
	path('/<int:movie_id>', MovieInfoView.as_view()),
	path('/<int:movie_id>/wish', Wish.as_view()),
	path('/<int:movie_id>/comment', MovieCommentView.as_view()),
	path('/<int:movie_id>/comment/<int:comment_id>', MovieCommentView.as_view()),
	path('/comment/like', CommentLikeView.as_view()),
	path('/<int:movie_id>/rating', Rating.as_view()),
]