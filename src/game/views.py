from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.contrib import messages
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

def detail(request, player_id) :
    player = get_object_or_404(Player, pk=player_id)

    register_form = ModifyUserForm(instance= player.user)
    player_form = PlayerForm(instance=player)

    return render(request, 'game/detail.html', {'player' : player, 'register_form': register_form, 'player_form': player_form, 'player_json' : player.getJSON()})

def delete(request, player_id) :
    if request.user.is_authenticated :
        if request.user.id == player_id :
            player = get_object_or_404(Player, pk=player_id)
            player.delete()
            return HttpResponseRedirect(reverse('game:index'))
        else :
            messages.error(request, "Tu ne peux pas supprimer un autre joueur que toi petit malin")
            return HttpResponseRedirect(reverse('game:index'))
    else :
        messages.error(request, "Il faut être connecté pour pouvoir supprimer un joueur")
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