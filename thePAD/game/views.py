from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic
from django.db.models import Count

from .models import Action, User


class IndexView(generic.ListView) :
    template_name = 'game/index.html'
    context_object_name = 'user_list'

    def get_queryset(self) :
        return User.objects.annotate(count=Count('action__point')).order_by('-count')

class DetailView(generic.DetailView) :
    model = User
    template_name = 'game/detail.html'

class PointView(generic.DetailView) :
    model = User
    template_name = 'game/points.html'

def attribute(request, user_id):
    user = get_object_or_404(User, pk=user_id)
    try :
        if request.POST['date'] == "" :
            action = Action(user = user, point = request.POST['point'])
        else :
            action = Action(user = user, point = request.POST['point'], act_date = request.POST['date'])
    except (KeyError, User.DoesNotExist) :
        return render(request, 'game/detail.html', {
            'user': user,
            'error_message': "Les entrées ne sont pas valides",
        })
    else :
        action.save()
        return HttpResponseRedirect(reverse('game:points', args=(user.id,)))

def delete(request, user_id) :
    user = get_object_or_404(User, user_id)
    #user = User.objects.get(pk=user_id)
    user.delete()
    return HttpResponseRedirect(reverse('game:index'))

def create_user(request) :
    try :
        name = request.POST["nom"]
    except (KeyError) :
        return render(request, 'game/index.html', {
            'error_message': 'Les entrées ne sont pas valides'
        })
    else :
        user = User(name=name)
        user.save()
        return HttpResponseRedirect(reverse('game:detail', args=(user.id,)))