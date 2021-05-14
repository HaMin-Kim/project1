import jwt

from django.http import JsonResponse

from users.models import User
from my_settings  import SECRET


def login_confirm(original_function):
    def wrapper(self, request):
        try:
            token = request.headers.get("Authorization", None)

            if token:
                token_payload = jwt.decode(token, SECRET, algorithms='HS256')

                if not User.objects.filter(id=token_payload['user_id']).exists():
                    return JsonResponse({'INVALID_TOKEN'})

                user          = User.objects.get(id=token_payload['user_id'])
                request.user  = user
                return original_function(self, request)

            return JsonResponse({'MESSAGE': 'NEED_LOGIN'}, status=401)

        except jwt.ExpiredSignatureError:
            return JsonResponse({'MESSAGE': 'EXPIRED_TOKEN'}, status=401)

        except jwt.DecodeError:
            return JsonResponse({'MESSAGE': 'INVALID_USER'}, status=401)

        except User.DoesNotExist:
            return JsonResponse({'MESSAGE': 'INVALID_USER'}, status=401)

    return wrapper