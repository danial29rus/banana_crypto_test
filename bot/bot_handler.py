from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from tasks.models import Task, UserProfile


@csrf_exempt
def link_account(request):
    if request.method == 'POST':
        telegram_username = request.POST['telegram_username']
        telegram_id = request.POST['telegram_id']
        unique_code = request.POST['unique_code']

        try:
            user_profile = UserProfile.objects.get(unique_code=unique_code)
            user_profile.telegram_username = telegram_username
            user_profile.telegram_id = telegram_id
            user_profile.save()
            return JsonResponse({"message": "Account linked successfully"}, status=200)
        except UserProfile.DoesNotExist:
            return JsonResponse({"error": "Unique code does not exist"}, status=400)
    else:
        return JsonResponse({"error": "Invalid request"}, status=400)


@csrf_exempt
def create_task(request):
    if request.method == 'POST':
        telegram_id = request.POST.get('telegram_id')
        title = request.POST.get('title')
        description = request.POST.get('description')
        try:
            user_profile = UserProfile.objects.get(telegram_id=telegram_id)
            task = Task.objects.create(user=user_profile.user, title=title, description=description)
            return JsonResponse({"status": "success", "task_id": task.id}, status=201)
        except UserProfile.DoesNotExist:
            return JsonResponse({"error": "Telegram ID does not exist"}, status=400)
    else:
        return JsonResponse({"error": "Invalid request method"}, status=405)




def get_tasks(request):
    if request.method == 'GET':
        telegram_id = request.GET.get('telegram_id')
        try:
            user_profile = UserProfile.objects.get(telegram_id=telegram_id)
            tasks = Task.objects.filter(user=user_profile.user)
            tasks_list = [
                {"id": task.id, "title": task.title, "description": task.description, "completed": task.completed} for
                task in tasks]
            return JsonResponse(tasks_list, safe=False)
        except UserProfile.DoesNotExist:
            return JsonResponse({"error": "Telegram ID does not exist"}, status=400)

    else:
        return JsonResponse({"error": "Invalid request method"}, status=405)