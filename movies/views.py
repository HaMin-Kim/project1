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
			
#			LIMIT = 10
			similar_movies = []
#			for similar_movie in movie.genre:
#				similar_movies.append(
#					{
#						'id'           : similar_movie.id,
#						'korean_title' : similar_movie.korean_title,
#						'thumbnail_img': similar_movie.thumbnail_img,
#						'netflix'      : similar_movie.netflix,
#						'watcha'       : similar_movie.watcha,
#					}
#				)
	
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
                                'genre'         : 
				'comments'      : movie_comments,
				'similar_movies': similar_movies,
				}

		return JsonResponse({'movie_information': movie_information}, status = 200)	
