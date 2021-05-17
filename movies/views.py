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
			netflix_random_data = Movie.objects.filter(netflix=True).values(
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
			watcha_random_data = Movie.objects.filter(watcha=True).values(
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

# 하나의 api에 3개의 엔드포인트를 만들어야한다.
# return 값이 3개다
# 박승오피스 순위 대로 나열할 경우
# 넷플릭스 추천 대로
# 왓챠 추천대
