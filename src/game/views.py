from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.contrib import messages
from django.db.models import Sum
from participants.forms import ModifyUserForm
from django.contrib.auth.models import User
from .forms import PlayerForm, ActionForm
from .models import Action, Player

import json
from datetime import date, datetime

def json_serial(obj):
    """JSON serializer for objects not serializable by default json code"""

    if isinstance(obj, (datetime, date)):
        return obj.isoformat()
    raise TypeError ("Type %s not serializable" % type(obj))

def index(request) :
    player_list = Player.objects.annotate(total_points=Sum('action__point')).order_by('-total_points')
    json_player_list = get_proper_JSON_from_player_list(player_list)
    print(json_player_list)
    return render(request, 'game/index.html', {'player_list' : player_list, 'json_player_list' : json_player_list})

def get_proper_JSON_from_player_list(player_list) :
    # Format du tableaux des actions :
    #   Date | Score J1 | Score J2 | ...
    tableau_final = []
    names = []

    # Première étape enregistrer toutes les actions
    for player in player_list :
        json_player = json.loads(player.getJSON())
        names.append(json_player['name'])
        for action in json_player["actions"] :
            base_ligne = [datetime.fromisoformat(action['date_action'])] + [None]*len(player_list)
            base_ligne[len(names)] = action['tot_score']
            tableau_final.append(base_ligne)

    # Process pour remplir le tableau
    # Sort
    tableau_final.sort(key= lambda row : row[0])
    tableau_score = [0]*len(names)

    player_list_dict = {'names' : names,
                        'actions' : []}

    for action in tableau_final :
        for index, val in enumerate(action[1:]) :
            if val == None :
                action[index + 1] = tableau_score[index]
            elif isinstance(val, int) :
                tableau_score[index] = val
        di = dict(zip(names, action[1:]))
        di["Date"] = action[0]
        player_list_dict["actions"].append(di)
        
    print(player_list_dict)

    return json.dumps(player_list_dict, default=json_serial)

def detail(request, player_id) :
    player = get_object_or_404(Player, pk=player_id)

    register_form = ModifyUserForm(instance= player.user)
    player_form = PlayerForm(instance=player)

    return render(request, 'game/detail.html', {'player' : player, 'register_form': register_form, 'player_form': player_form, 'player_json' : player.getJSON()})

def delete(request, player_id) :
    if request.user.is_authenticated :
        player = get_object_or_404(Player, pk=player_id)
        if request.user.id == player.user.id :
            user = get_object_or_404(User, pk=player.user.id)
            user.delete()
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