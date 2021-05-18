from django.urls import path

<<<<<<< HEAD
from users.views import SignUp, SignIn, Review, StarDistribution
=======
from users.views import SignUp, SignIn, MyPage, Review
>>>>>>> main

urlpatterns = [
    path("/signup", SignUp.as_view()),
    path("/signin", SignIn.as_view()),
<<<<<<< HEAD
    path("/review", Review.as_view()),
    path("/analysis", StarDistribution.as_view()),
]
=======
    path("/mypage", MyPage.as_view()),
    path("/review", Review.as_view())
]
>>>>>>> main
