import json
import bcrypt
import jwt
import re

from django.http import JsonResponse
from django.views import View

from users.models import User
from my_settings import SECRET

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

            return JsonResponse({"MESSAGE" : "SUCCESS"}, status=200)

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