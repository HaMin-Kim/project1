import json, random

from django.views     import View
from django.http      import JsonResponse
from django.db.models import Max

from users.utils      import login_confirm
from movies.models    import Movie, Comment, Like, Genre, MovieGenre

class MovieInformationView(View):
	def get(self, request, movie_id):
		if Movie.objects.filter(id=movie_id).exists():
			movie    = Movie.objects.get(id = movie_id)

			movie_comments = []
		#	for comment in Comment.objects.filter(movie = movie):
		#		movie_comments.append(
		#			{
		#				'id'     : comment.id,
		#				'user'   : comment.user,
		#				'comment': comment.comment,
		#			#	'likes'  : comment.like_set.
		#			}
		#		)
			
			LIMIT = 10
			similar_movies = []
			genre = MovieGenre
			for similar_movie in movie.genre.all():
				similar_movies.append(
					{
						'id'           : similar_movie.id,
						'korean_title' : similar_movie.movie_set.korean_title,
						'thumbnail_img': similar_movie.movie_set.thumbnail_img,
						'netflix'      : similar_movie.movie_set.netflix,
						'watcha'       : similar_movie.movie_set.watcha,
					}
				)
	
			movie_information = {
                                'id'            : movie.id,
                                'korean_title'  : movie.korean_title,
                                'english_title' : movie.english_title,
                                'country'       : movie.country,
                                'release_date'  : movie.release_date,
                                'running_time'  : movie.running_time,
                                'discription'   : movie.discription,
                                'thumbnail_img' : movie.thumbnail_img,
                                'background_img': movie.background_img,
                                'genre'         : movie.genre.name,
				'comments'      : movie_comments,
				'similar_movies': similar_movies,
				}

		return JsonResponse({'movie_information': movie_information}, status = 200)
	
#	def post(self, request, comment_id):
#		data = json.loads(request.body)
#	#	try:
#			movie_check = Movie.objects.filter(id=data["movieId"])
#			
#            	# 영화가 없을 경우
#			if not movie_check.exists():
#				return JsonResponse({"message": "NO_MOVIE"}, status=40)
#			
#			comment_check = Comment.objects.filter(
#                	user_id=request.user.id,
#                	movie_id=data["movieId"]
#            		)
#	def patch(self, request, comment_id)

#	def delete(self, request, comment_id)

# 상세페이지 정보 주기(댓글 좋아요 순으로 뿌려주기, 영화 관객순으로 뿌려주기)
# 댓글기능(추가,수정,삭제)
# 좋아요 누르기 기능
# 장바구니 추가 기능
