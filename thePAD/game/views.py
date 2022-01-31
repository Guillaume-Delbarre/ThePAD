from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic

from .models import Action, User


class IndexView(generic.ListView) :
    template_name = 'game/index.html'
    context_object_name = 'user_list'

    def get_queryset(self) :
        return User.objects.all()

class DetailView(generic.DetailView) :
    model = User
    template_name = 'game/detail.html'

class PointView(generic.DetailView) :
    model = User
    template_name = 'game/points.html'
        
# def index(request):
#     user_list = User.objects.all()
#     context = {'user_list': user_list}
#     return render(request, 'game/index.html', context)

# def detail(request, user_id):
#     user = get_object_or_404(User, pk=user_id)
#     return render(request, 'game/detail.html', {'user': user})

# def points(request, user_id):
#     user = get_object_or_404(User, pk=user_id)
#     return render(request, 'game/points.html', {'user': user})

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