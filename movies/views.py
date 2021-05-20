import json

from django.views     import View
from django.http      import JsonResponse

from users.utils      import login_confirm
from movies.models    import Movie, Comment, Like, Genre, MovieGenre, RatingMovie


class MovieInfoView(View):
	@ login_confirm2
	def get(self, request, movie_id):
		if Movie.objects.filter(id = movie_id).exists():
			movie = Movie.objects.get(id = movie_id)
			user  = request.user
		
			# 보고싶어요
			wish_movie = WishMovie.objects.filter(user = user, movie = movie.id)
			if wish_movie.exists():
				wish_check = 1

			elif not wish_movie.exists():
                        	wish_check = 0

			# 별점 
			rating_movie = RatingMovie.objects.filter(user = user, movie = movie.id)
			if rating_movie.exists():
				star_check = rating_movie.rating

			elif rating_movie.exists():
				star_check = 0

			movie_comments = [
				{
					'id'       : comment.id,
					'user_id'  : comment.user.id,
					'user_name': comment.user.name,
					'comment'  : comment.comment,
					'likes'    : comment.like_set.count()
				}
				for comment in Comment.objects.filter(movie=movie)
			]
			
			
			LIMIT = 3
			similar_movies = [list(similar_movie.movie_set.values(
			'id','korean_title', 'thumbnail_img', 'netflix', 'watcha'
			))[:LIMIT] for similar_movie in movie.genre.all()]
	
			movie_information = {
                                'id'            : movie.id,
                                'korean_title'  : movie.korean_title,
                                'english_title' : movie.english_title,
                                'country'       : movie.country,
                                'release_date'  : movie.release_date,
                                'running_time'  : movie.running_time,
                                'discription'   : movie.discription,
				'wish_check'    : wish_check,
                                'thumbnail_img' : movie.thumbnail_img,
                                'background_img': movie.background_img, 
				'genre'         : list(movie.genre.values('name')),
				'comments'      : movie_comments,
				'similar_movies': similar_movies,
				}

			return JsonResponse({'movie_information': movie_information}, status = 200)
		
		return JsonResponse({"message": "NO_MOVIE"}, status = 404)
