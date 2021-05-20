import json
import bcrypt
import jwt
import re
import random
import numpy

from django.http      import JsonResponse
from django.views     import View
from django.db.models import Avg, Q

from users.models  import User, RatingMovie, WishMovie
from movies.models import Movie, Genre
from my_settings   import SECRET
from users.utils   import login_confirm

class SignUp(View):
    def post(self, request):
        try:
            data                = json.loads(request.body)
            name                = data["name"]
            email               = data["email"]
            password            = data["password"]
            email_validation    = re.compile('^[a-z0-9]+@[a-z0-9]+\.[a-z0-9.]+$', re.I)
            password_validation = re.compile(r'^(?=.*[a-z])(?=.*[0-9])(?=.*[~!@#$%^&*]).{10,}', re.I)

            if not email_validation.match(email):
                return JsonResponse({"MESSAGE" : "INVALID_EMAIL"}, status=400)

            if User.objects.filter(email=email).exists():
                return JsonResponse({"MESSAGE" : "INVALID_USER"}, status=400)

            if not password_validation.match(password):
                return JsonResponse({"MESSAGE" : "INVALID_PASSWORD"}, status=400)

            byte_password   = password.encode("utf-8")
            encode_password = bcrypt.hashpw(byte_password, bcrypt.gensalt())
            decode_password = encode_password.decode("utf-8")

            User.objects.create(
                name     = name,
                email    = email,
                password = decode_password
            )

            return JsonResponse({"MESSAGE" : "SUCCESS"}, status=201)

        except KeyError:
            return JsonResponse({"MESSAGE" : "KEY_ERROR"}, status=400)

class SignIn(View):
    def post(self, request):
        try:
            data     = json.loads(request.body)
            email    = data["email"]
            password = data["password"]

            if not User.objects.filter(email = email):
                return JsonResponse({"MESSAGE" : "INVALID_USER"}, status=400)

            user = User.objects.get(email = email)

            if not bcrypt.checkpw(password.encode("utf-8"), user.password.encode("utf-8")):
                return JsonResponse({"MESSAGE" : "INVALID_PASSWORD"}, status=400)

            token = jwt.encode({"user_id" : user.id}, SECRET, algorithm="HS256")

            return JsonResponse({"MESSAGE" : "SUCCESS", "token" : token}, status=200)

        except KeyError:
            return JsonResponse({"MESSAGE" : "KEY_ERROR"}, status=400)

class MyPage(View):
    @login_confirm
    def get(self, request):
        user         = request.user
        rating_count = len(RatingMovie.objects.filter(user = user))
        wish         = len(WishMovie.objects.filter(user = user))
        result       = {"name" : user.name, "rating_count" : rating_count, "wish_count" : wish}

        return JsonResponse({"result" : result}, status = 200)

class StarDistribution(View):
    @login_confirm
    def get(self, request):
        user              = request.user
        user_movies       = RatingMovie.objects.filter(user=user)
        rating_count      = len(user_movies)
        rating_highest    = float(user_movies.order_by("-rating")[0].rating)
        rating_average    = float(user_movies.aggregate(Avg("rating"))['rating__avg'])
        star_distribution = [{rating : len(RatingMovie.objects.filter(user=user, rating=rating))} for rating in numpy.arange(0.5, 5.5, 0.5)]

        result = {
                "rating_count"      : rating_count,
                "rating_highest"    : rating_highest,
                "rating_average"    : rating_average,
                "star_distribution" : star_distribution
                }

        return JsonResponse({"result" : result}, status=200)

#추가기능 구현 사항
class Review(View):
    @login_confirm
    def get(self, request):
        max_id        = Movie.objects.last().id
        random_list   = random.sample(range(1, max_id+1), max_id)
        user          = request.user
        rating        = 0
        rating_movies = len(RatingMovie.objects.filter(user=user))
        movie_list    = Movie.objects.all()
        genre_id      = request.GET.get("genre_id", None)
        q             = Q(user = user)
        
        #쿼리 파라미터로 받은 장르 id 값이 있을 경우
        if genre_id:
            genre       = Genre.objects.get(id = genre_id)
            genre_movie = [
                {
                    "movie_id"     : movie.id,
                    "title"        : movie.korean_title,
                    "country"      : movie.country,
                    "release_date" : movie.release_date,
                    "rating"       : rating,
                    "thumbnail"    : movie.thumbnail_img
                    }
                    for movie in Movie.objects.filter(genre = genre)\
                        if not RatingMovie.objects.filter(q, movie=movie).exists()
                        ]

            return JsonResponse({"genre_movie" : genre_movie}, status=200)
            
        #쿼리 파라미터로 받은 값이 없을 경우 그대로 랜덤 영화 목록 반환    
        movie_random = [
            {
                "movie_id"     : movie.id,
                "title"        : movie.korean_title,
                "country"      : movie.country,
                "release_date" : movie.release_date,
                "rating"       : rating,
                "thumbnail"    : movie.thumbnail_img
                } 
                for movie_id in random_list for movie in movie_list\
                    if movie.id == movie_id if not RatingMovie.objects.filter(q, movie = movie.id).exists()
                    ]
        
        movie_random.append({"rating_movies": rating_movies})

        return JsonResponse({"movie_random" : movie_random}, status=200)

    @login_confirm
    def post(self, request):
        try:
            data   = json.loads(request.body)
            rating = float(data["rating"])
            movie  = Movie.objects.get(id = data["movie"])
            user   = request.user
            q      = Q(movie = movie) & Q(user = user)

            if RatingMovie.objects.filter(q).exists():
                user_movie = RatingMovie.objects.get(q)

                if user_movie.rating == rating:
                    user_movie.delete()

                    return JsonResponse({"MESSAGE" : "DELETE_SUCCESS"}, status=204)

                user_movie.rating = rating
                user_movie.save()

                return JsonResponse({"MESSAGE" : "UPDATE_SUCCESS"}, status=201)

            RatingMovie.objects.create(movie=movie, user=user, rating=rating)

            return JsonResponse({"MESSAGE" : "CREATE_SUCCESS"}, status=201)


        except KeyError:
            return JsonResponse({"MESSAGE" : "KEY_ERROR"})