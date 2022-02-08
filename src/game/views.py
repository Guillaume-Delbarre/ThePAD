from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic
from django.db.models import Count

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

def create_player(request) :
    try :
        name = request.POST["nom"]
        photo = request.POST["photo"]
        description = request.POST["description"]
    except (KeyError) :
        return render(request, 'game/index.html', {
            'error_message': 'Les entrées ne sont pas valides'
        })
    else :
        player = Player(name=name, photo=photo, description=description)
        player.save()
        return HttpResponseRedirect(reverse('game:detail', args=(player.id,)))

def best(request) :
    player = Player.objects.annotate(count=Count('action__point')).order_by('-count').first()
    return HttpResponseRedirect(reverse('game:points', args=(player.id,)))