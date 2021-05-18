import json

from django.views     import View
from django.http      import JsonResponse

from users.utils      import login_confirm
from movies.models    import Movie, Comment
from users.models     import User

class MovieCommentView(View):
	@login_confirm
	def post(self, request, movie_id):
		data = json.loads(request.body)
		
		try:
			# 사용자 확인
			comment_check = Comment.objects.filter(user = request.user)

			# 댓글이 이미 있는 경우
			if comment_check.exists():
                		return JsonResponse({"MESSAGE": "ALREADY_EXIST"}, status=400)

			# 댓글이 처음이면 생성
			comment = Comment.objects.create(
				movie   = Movie.objects.get(id = movie_id),
				user    = request.user,
				comment = data["comment"]
			)
			return JsonResponse({'MESSAGE': 'SUCCESS'}, status =200)

		except KeyError:
			return JsonResponse({"message": "KEY_ERROR"}, status=400)
	
	@login_confirm
	def patch(self, request, movie_id, comment_id):
		data = json.loads(request.body)
		
		try:
                        # 댓글 확인
			comment_check = Comment.objects.filter(id=comment_id)
			
			# 댓글이 없는 경우
			if not comment_check.exists():
				return JsonResponse({"message": "NO_COMMENT"}, status=400)
	
			# 댓글이 있으면
			comment = comment_check.first()
			comment.comment = data["comment"]
			comment.save()

			update_comment = {"comment": comment.comment}
			return JsonResponse(update_comment, status=200)

		except KeyError:
                        return JsonResponse({"message": "KEY_ERROR"}, status=400)
	
	@login_confirm
	def delete(self, request, movie_id, comment_id):
		# 댓글 확인
		comment_check = Comment.objects.filter(id=comment_id)

		 # 댓글이 없는 경우
		if not comment_check.exists():
			return JsonResponse({"message": "NO_COMMENT"}, status=404)

		comment_check.delete()
		
		return JsonResponse({"message": "SUCCESS"}, status=204)
		
	@login_confirm
	def get(self, request, movie_id, comment_id):
		results = []
		comment_check = Comment.objects.filter(user = request.user)
		
		# 댓글이 없는 경우
		if not comment_check.exists():
			return JsonResponse({"message": "NO_COMMENT"}, status=400)
		
		# 댓글이 있을 경우
		comment = comment_check.first()
		
		my_comment_data = {
					'my_id'     : comment.user.id,
					'my_name'   : comment.user.name,
					'my_comment': comment.comment,
				}
		results.append(my_comment_data)
		return JsonResponse({'results': results}, status=200)


