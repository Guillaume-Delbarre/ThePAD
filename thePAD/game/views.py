from django.http import HttpResponse
from django.template import loader

from .models import User


def index(request):
    user_list = User.objects.all()
    template = loader.get_template('game/index.html')
    context = {
        'user_list': user_list,
    }
    return HttpResponse(template.render(context, request))

def detail(request, user_id):
    return HttpResponse("You're looking at user %s." % user_id)

def points(request, user_id):
    return HttpResponse("You're looking at the points of user %s." % user_id)

def attribute(request, user_id):
    return HttpResponse("You're adding point for user %s." % user_id)