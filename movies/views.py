import json

from django.views     import View
from django.http      import JsonResponse
from django.db.models import Q

from users.utils      import login_confirm
from movies.models    import Movie, Comment

class MovieMainView(View):
	def get(self, request):
		ranking         = request.GET.get('ranking')
		provider        = request.GET.get('provider')
		results = []
		q = Q()

		LIMIT   = 10
		orderby = '?'
		if ranking == 'box-office':
			q       = Q()
			data    = 'movie_ranking_data'
			LIMIT   = 25
			orderby = '-audience_count'

		if provider == 'netflix':
			q       = Q(netflix = True)
			data    = 'netflix_random_data'

		if provider == 'watcha':
			q       = Q(watcha = True)
			data    = 'watcha_random_data'

		data  = Movie.objects.filter(q).values(
						'id',
						'korean_title', 
						'english_title',
						'country', 
						'release_date',
						'thumbnail_img',
						'netflix',
						'watcha',
					).order_by(orderby)[:LIMIT]
		results.append(list(data))

		return JsonResponse({'MESSAGE': results}, status = 200)

