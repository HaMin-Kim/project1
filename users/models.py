from django.db import models

class User(models.Model):
    name      = models.CharField(max_length = 45)
    email     = models.CharField(max_length = 45, unique = True)
    password  = models.CharField(max_length = 250)
    create_at = models.DateTimeField(auto_now_add = True)
    update_at = models.DateTimeField(auto_now = True)
    wish      = models.ManyToManyField('movies.Movie', through = "WishMovie", related_name = "wish")
    rating    = models.ManyToManyField('movies.Movie', through = "RatingMovie", related_name = 'rating' )

    class Meta:
        db_table = "users"

    def __str__(self):
        return self.email

class RatingMovie(models.Model):
    user  = models.ForeignKey('User', on_delete = models.CASCADE)
    movie = models.ForeignKey('movies.Movie', on_delete = models.CASCADE)

    class Meta:
        db_table = 'raing_movies'

class WishMovie(models.Model):
    user   = models.ForeignKey('User', on_delete = models.CASCADE)
    movie  = models.ForeignKey('movies.Movie', on_delete = models.CASCADE)
    rating = models.DecimalField(max_digits = 2, decimal_places = 1, null=True)
    wish   = models.BooleanField(default = False)

    class Meta:
        db_table = "wish_movies"
