import json
import bcrypt
import jwt
import re
import random

from django.http      import JsonResponse
from django.views     import View
from django.db.models import Max

from users.models  import User, RatingMovie
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

class Review(View):
    @login_confirm
    def get(self, request):
        result        = []
        genre_list    = [(i.id ,i.name) for i in Genre.objects.all()]
        max_id        = Movie.objects.all().aggregate(max_id = Max("id"))['max_id']
        random_list   = random.sample(range(1, max_id+1), max_id)
        user          = request.user
        rating        = 0
        genre         = None
        rating_movies = len(RatingMovie.objects.filter(user=user))

        for movies in random_list:

            if Movie.objects.filter(id = movies).exists():

                if not RatingMovie.objects.filter(movie=movies, user=user).exists():
                    movie = Movie.objects.get(id=movies)

                    if movie.genre.filter(movie=movie).exists():
                        genre = movie.genre.get(movie=movie).name

                    result.append(
                        {
                            "movie_id"     : movie.id,
                            "title"        : movie.korean_title,
                            "country"      : movie.country,
                            "release_date" : movie.release_date,
                            "rating"       : rating,
                            "genre"        : genre,
                            "thumbnail"    : movie.thumbnail_img
                        }
                    )

        return JsonResponse(
            {
                "result"        : result,
                "genre"         : genre_list,
                "rating_movies" : rating_movies
            },status=200
        )