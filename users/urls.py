from django.urls import path

from users.views import SignUp, SignIn, MyPage

urlpatterns = [
    path("/signup", SignUp.as_view()),
    path("/signin", SignIn.as_view()),
    path("/mypage", MyPage.as_view())
]
