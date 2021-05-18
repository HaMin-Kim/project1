from django.urls import path

from users.views import SignUp, SignIn, Review, StarDistribution

urlpatterns = [
    path("/signup", SignUp.as_view()),
    path("/signin", SignIn.as_view()),
    path("/review", Review.as_view()),
    path("/analysis", StarDistribution.as_view()),
]
