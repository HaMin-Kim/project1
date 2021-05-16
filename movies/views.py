import json, random

from django.views     import View
from django.http      import JsonResponse
from django.db.models import Max

from users.utils      import login_confirm
from movies.models    import Movie, Comment

class MainPageView(View):
	def get(self, request):
		RANKING_LIMIT = 25
		movie_ranking_data = Movie.objects.values(
			'id', 'korean_title', 'country', 'release_date', 'thumbnail_img',
		).order_by('-audience_count')[:RANKING_LIMIT]

		RANDOM_LIMIT = 10
		netflix_random_data = Movie.objects.filter(netflix=True).values(
                        'id', 'korean_title', 'country', 'release_date', 'thumbnail_img',
                ).order_by('?')[:RANDOM_LIMIT]

		watcha_random_data = Movie.objects.filter(watcha=True).values(
                        'id', 'korean_title', 'country', 'release_date', 'thumbnail_img',
                ).order_by('?')[:RANDOM_LIMIT]

		return JsonResponse({
			'박스오피스 순위': list(movie_ranking_data),
			'넷플릭스 추천': list(netflix_random_data), 
			'왓챠 추천': list(watcha_random_data),
		}, status = 200)
		
			

		

		
		
	
