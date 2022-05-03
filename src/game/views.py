from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic
from django.db.models import Count
from participants.forms import ModifyUserForm
from .forms import PlayerForm, ActionForm
from .models import Action, Player


class IndexView(generic.ListView) :
    template_name = 'game/index.html'
    context_object_name = 'player_list'

    def get_queryset(self) :
        return Player.objects.annotate(count=Count('action__point')).order_by('-count')

class DetailView(generic.DetailView) :
    model = Player
    template_name = 'game/detail.html'

class PointView(generic.DetailView) :
    model = Player
    template_name = 'game/points.html'

def detail(request, player_id) :
    player = get_object_or_404(Player, pk=player_id)

    register_form = ModifyUserForm(instance= player.user)
    player_form = PlayerForm(instance=player)

    return render(request, 'game/detail.html', {'player' : player, 'register_form': register_form, 'player_form': player_form})


def attribute(request, player_id):
    player = get_object_or_404(Player, pk=player_id)
    try :
        if request.POST['date'] == "" :
            action = Action(player = player, point = request.POST['point'])
        else :
            action = Action(player = player, point = request.POST['point'], act_date = request.POST['date'])
    except (KeyError, Player.DoesNotExist) :
        return render(request, 'game/detail.html', {
            'player': player,
            'error_message': "Les entrées ne sont pas valides",
        })
    else :
        action.save()
        return HttpResponseRedirect(reverse('game:points', args=(player.id,)))

def delete(request, player_id) :
    player = get_object_or_404(Player, pk=player_id)
    #player = Player.objects.get(pk=player_id)
    player.delete()
    return HttpResponseRedirect(reverse('game:index'))

def add_action(request) :
    submitted = False
    if request.method == "POST" :
        form = ActionForm(request.POST, request.FILES)
        if form.is_valid() :
            form.save()
            return HttpResponseRedirect('/add_action?submitted=True')
    else :
        form = ActionForm
        if 'submitted' in request.GET :
            submitted = True
        
    return render(request, 'game/add_action.html', {'form':form, 'submitted':submitted})