from django.db import models

class Movie(models.Model):
    korean_title   = models.CharField(max_length = 45)
    english_title  = models.CharField(max_length = 45)
    country        = models.CharField(max_length = 45)
    release_date   = models.DateField(null = True)
    running_time   = models.IntegerField()
    discription    = models.TextField(null = True)
    audience_count = models.IntegerField()
    thumbnail_img  = models.URLField()
    background_img = models.URLField()
    category       = models.ForeignKey('Category', on_delete = models.CASCADE)
    genre_id       = models.ManyToManyField('Genre', through = 'Movie_Genre')
    provider_id    = models.ManyToManyField('Provider', through = 'Movie_Provider')
    director_id    = models.ManyToManyField('Director', through = 'Movie_Director')
    actor_id       = models.ManyToManyField('Actor', through = 'Movie_Actor')
    comment_id     = models.ManyToManyField('users.User', through = "Comment", related_name='user')

    class Meta:
        db_table = 'movies'

    def __str__(self):
        return self.korean_title

class Category(models.Model):
    name = models.CharField(max_length = 45)

    class Meta:
        db_table = 'categories'

    def __str__(self):
        return self.name

class Genre(models.Model):
    name = models.CharField(max_length = 45)

    class Meta:
        db_table = 'genres'

    def __str__(self):
        return self.name

class Movie_Genre(models.Model):
    genre_id = models.ForeignKey('Genre', on_delete = models.CASCADE)
    movie_id = models.ForeignKey('Movie', on_delete = models.CASCADE)
    class Meta:
        db_table = 'categories_genres'

class Provider(models.Model):
    netflix = models.BooleanField(default = False)
    watcha  = models.BooleanField(default = False)

    class Meta:
        db_table = 'providers'

    def __str__(self):
        return self.name

class Movie_Provider(models.Model):
    movie_id    = models.ForeignKey('Movie', on_delete = models.CASCADE)
    provider_id = models.ForeignKey('Provider', on_delete = models.CASCADE)

    class Meta:
        db_table = 'movies_providers'

class Director(models.Model):
    first_name    = models.CharField(max_length = 45)
    last_name     = models.CharField(max_length = 45, blank = True)
    gender        = models.CharField(max_length = 30)
    date_of_birth = models.DateField(null = True)

    class Meta:
        db_table = 'directors'

    def __str__(self):
        return self.first_name

class Movie_Director(models.Model):
    movie    = models.ForeignKey('Movie', on_delete = models.CASCADE)
    director = models.ForeignKey('Director', on_delete = models.CASCADE)

    class Meta:
        db_table = 'movies_directors'

class Actor(models.Model):
    first_name    = models.CharField(max_length = 45)
    last_name     = models.CharField(max_length = 45, blank = True)
    gender        = models.CharField(max_length = 30)
    date_of_birth = models.DateField(null = True)

    class Meta:
        db_table = 'actors'

    def __str__(self):
        return self.first_name

class Movie_Actor(models.Model):
    movie_id = models.ForeignKey('Movie', on_delete = models.CASCADE)
    actor_id = models.ForeignKey('Actor', on_delete = models.CASCADE)

    class Meta:
        db_table = 'movies_actors'

class Comment(models.Model):
    movie   = models.ForeignKey('Movie', on_delete = models.CASCADE)
    user    = models.ForeignKey('users.User', on_delete = models.CASCADE)
    comment = models.TextField()

    class Meta:
        db_table = "comments"

class Like(models.Model):
    comment = models.ForeignKey("Comment", on_delete = models.CASCADE)
    user    = models.ForeignKey('users.User', on_delete = models.CASCADE)

    class Meta:
        db_table = "likes"
