import json

from django.views     import View
from django.http      import JsonResponse
from django.db.models import Q

from users.utils      import login_confirm
from movies.models    import Movie, Comment

class MovieInfoView(View):
	def get(self, request):
		ranking         = request.GET.get('ranking')
		provider        = request.GET.get('provider')
		results = []
		q = Q()

		if ranking == 'box-office':
			LIMIT = 25
			movie_ranking_data = Movie.objects.values(
						'id',
                                                'korean_title',
                                                'country',
                                                'release_date',
                                                'thumbnail_img'
						'netflix',
						'watcha',
                                                ).order_by('-audience_count')[:LIMIT]
			results.append(list(movie_ranking_data))
		
		if provider == 'netflix':
			LIMIT = 10
			netflix_random_data = Movie.objects.filter(Q(netflix=True)).values(
						'id',
						'korean_title', 
						'country', 
						'release_date',
						'thumbnail_img',
						'netflix',
						'watcha',
						).order_by('?')[:LIMIT]
			results.append(list(netflix_random_data))

		if provider == 'watcha':
			LIMIT = 10
			watcha_random_data = Movie.objects.filter(Q(watcha=True)).values(
						'id',
						'korean_title',
                                                'country',
                                                'release_date',
                                                'thumbnail_img',
						'netflix',
						'watcha',
                                                )[:LIMIT]
			results.append(list(watcha_random_data))

		return JsonResponse({'MESSAGE': results}, status = 200)

