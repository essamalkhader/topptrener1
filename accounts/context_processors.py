from .models import TrainerProfile


def user_role(request):
    is_trainer = False
    if request.user.is_authenticated:
        is_trainer = TrainerProfile.objects.filter(user=request.user).exists()
    return {"is_trainer": is_trainer}