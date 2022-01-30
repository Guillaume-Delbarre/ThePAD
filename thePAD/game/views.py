from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render

from .models import User


def index(request):
    user_list = User.objects.all()
    context = {'user_list': user_list}
    return render(request, 'game/index.html', context)

def detail(request, user_id):
    user = get_object_or_404(User, pk=user_id)
    return render(request, 'game/detail.html', {'user': user})

def points(request, user_id):
    return HttpResponse("You're looking at the points of user %s." % user_id)

def attribute(request, user_id):
    return HttpResponse("You're adding point for user %s." % user_id)