import json

from django.views     import View
from django.http      import JsonResponse
from django.db.models import Q

from users.utils      import login_confirm, Detail_login_confirm
from movies.models    import Movie, Comment, Like, Genre, MovieGenre
from users.models     import User, RatingMovie, WishMovie

class MovieMainView(View):
	def get(self, request):
		ranking         = request.GET.get('ranking')
		provider        = request.GET.get('provider')
		results = []
		q = Q()

		LIMIT   = 10
		orderby = '?'
		if ranking == 'box-office':
			q       = Q()
			data    = 'movie_ranking_data'
			LIMIT   = 25
			orderby = '-audience_count'

		if provider == 'netflix':
			q       = Q(netflix = True)
			data    = 'netflix_random_data'

		if provider == 'watcha':
			q       = Q(watcha = True)
			data    = 'watcha_random_data'

		data  = Movie.objects.filter(q).values(
						'id',
						'korean_title', 
						'english_title',
						'country', 
						'release_date',
						'thumbnail_img',
						'netflix',
						'watcha',
					).order_by(orderby)[:LIMIT]
		results.append(list(data))

		return JsonResponse({'MESSAGE': results}, status = 200)

class MovieCommentView(View):
	@login_confirm
	def post(self, request, movie_id):
		data = json.loads(request.body)
		
		try:
			# 사용자 확인
			comment_check = Comment.objects.filter(user = request.user)

			# 댓글이 이미 있는 경우
			if comment_check.exists():
                		return JsonResponse({"MESSAGE": "ALREADY_EXIST"}, status=400)

			# 댓글이 처음이면 생성
			comment = Comment.objects.create(
				movie   = Movie.objects.get(id = movie_id),
				user    = request.user,
				comment = data["comment"]
			)
		
			comment_id = {"id":comment.id}
			return JsonResponse({'comment_id': comment.id}, status =201)

		except KeyError:
			return JsonResponse({"message": "KEY_ERROR"}, status=400)
	
	@login_confirm
	def patch(self, request, movie_id, comment_id):
		data = json.loads(request.body)
		
		try:
                        # 댓글 확인
			comment_check = Comment.objects.filter(id=comment_id)
			
			# 댓글이 없는 경우
			if not comment_check.exists():
				return JsonResponse({"message": "NO_COMMENT"}, status=400)
	
			# 댓글이 있으면
			comment = comment_check.first()
			comment.comment = data["comment"]
			comment.save()

			update_comment = {"comment": comment.comment}
			return JsonResponse(update_comment, status=201)

		except KeyError:
                        return JsonResponse({"message": "KEY_ERROR"}, status=400)
	
	@login_confirm
	def delete(self, request, movie_id, comment_id):
		# 댓글 확인
		comment_check = Comment.objects.filter(id=comment_id)

		 # 댓글이 없는 경우
		if not comment_check.exists():
			return JsonResponse({"message": "NO_COMMENT"}, status=404)

		comment_check.delete()
		
		return JsonResponse({"message": "SUCCESS"}, status=204)
		
	@login_confirm
	def get(self, request, movie_id, comment_id):
		movie         = Movie.objects.get(id = movie_id)
		comment_check = Comment.objects.filter(user = request.user)
		
		# 댓글이 없는 경우
		if not comment_check.exists():
			return JsonResponse({"message": "NO_COMMENT"}, status=400)
		
		# 댓글이 있을 경우
		comment = comment_check.first()
		
		my_comment_data = {
					'my_id'     : comment.user.id,
					'my_name'   : comment.user.name,
					'my_comment': comment.comment,
				}

		other_comment_data = [ {
					'id'       : comment.id,
					'user_id'  : comment.user.id,
					'user_name': comment.user.name,
					'comment'  : comment.comment,
					'likes'    : comment.like_set.count()
				} 
				for comment in Comment.objects.filter(movie=movie)]
	
		return JsonResponse({'my_comment_data': my_comment_data, 'other_comment_data': other_comment_data}, status=200)


class CommentLikeView(View):
	@login_confirm
	def post(self, request):
		data = json.loads(request.body)
	
		try:
			# 확인
			comment_check = Comment.objects.filter(id = data['comment_id'])
			like_check    = Like.objects.filter(
			user = request.user, comment = data['comment_id']
			)
		
			# 댓글이 없으면
			if not comment_check.exists():
				return JsonResponse({"message": "NO COMMENT"}, status=404)
		
			# 이미 좋아요를 한 경우 좋아요 삭제 처리
			if like_check.exists():
				like_check.delete()
				return JsonResponse({"message": "DELETE_SUCCESS"}, status=204)
		
			# 댓글이 있고 좋아요가 없으면
			Like.objects.create(
				user_id    = request.user.id,
				comment_id = data['comment_id']
                	)

			return JsonResponse({"message": "SUCCESS"}, status=201)
			
		except KeyError:
			return JsonResponse({"message": "KEY_ERROR"}, status=400)

class MovieInfoView(View):
	@ Detail_login_confirm
	def get(self, request, movie_id):
		if Movie.objects.filter(id = movie_id).exists():
			movie = Movie.objects.get(id = movie_id)

			star_check = 0
			wish_check = 0

			if request.user:
				rating_movie = RatingMovie.objects.filter(user=request.user, movie=movie.id)
				if rating_movie.exists():
					star_check = rating_movie.rating

				if WishMovie.objects.get(user = user, movie = movie.id).exists():
					wish_check   = 1

			
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
				'star_check'    : star_check,
                                'thumbnail_img' : movie.thumbnail_img,
                                'background_img': movie.background_img, 
				'genre'         : list(movie.genre.values('name')),
				'similar_movies': similar_movies,
				}

			return JsonResponse({'movie_information': movie_information}, status = 200)
		
		return JsonResponse({"message": "NO_MOVIE"}, status = 404)

class Rating(View):
    @login_confirm
    def post(self, request, movie_id):
        try:
            data   = json.loads(request.body)
            rating = float(data["rating"])
            user   = request.user
            movie  = Movie.objects.get(id = movie_id)
            
            if RatingMovie.objects.filter(movie = movie, user = user).exists():
                user_movie = RatingMovie.objects.get(movie = movie, user = user)
                
                if user_movie.rating == rating:
                    user_movie.delete()
                    
                    return JsonResponse({"MESSAGE" : "DELETE_SUCCESS"}, status=204)

                user_movie.rating = rating
                user_movie.save()
                return JsonResponse({"MESSAGE" : "UPDATE_SUCCESS"}, status=201)
                
            RatingMovie.objects.create(movie = movie, user = user, rating=rating)
            
            return JsonResponse({"MESSAGE" : "CREATE_SUCCESS"}, status=201)

        except KeyError:
            return JsonResponse({"MESSAGE" : "KEY_ERROR"}, status=400)

class Wish(View):
	@login_confirm
	def post(self, request, movie_id):
		user  = request.user
		movie = Movie.objects.get(id = movie_id)
		
		if WishMovie.objects.filter(user = user, movie = movie).exists():
			WishMovie.objects.get(user = user, movie = movie).delete()
			
			return JsonResponse({"MESSAGE" : "DELETE_SUCCESS"}, status=204)
			
		WishMovie.objects.create(user = user, movie = movie)
		
		return JsonResponse({"MESSAGE" : "CREATE_SUCCESS"}, status=201)
