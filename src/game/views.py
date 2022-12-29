from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse
from django.contrib import messages
from django.db.models import Sum
from participants.forms import ModifyUserForm
from django.contrib.auth.models import User
from .forms import PlayerForm, ActionForm
from .models import Action, Player, Mise, MiseJoueur, Pari

import json
from decimal import *
from datetime import date, datetime

def json_serial(obj):
    """JSON serializer for objects not serializable by default json code"""

    if isinstance(obj, (datetime, date)):
        return obj.isoformat()
    raise TypeError ("Type %s not serializable" % type(obj))

def index(request) :
    player_list = Player.objects.annotate(total_points=Sum('action__point')).order_by('-total_points')
    json_player_list = get_proper_JSON_from_player_list(player_list)
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
            print(val, type(val))
            if val == None :
                action[index + 1] = tableau_score[index]
            elif isinstance(val, str) :
                tableau_score[index] = val
        di = dict(zip(names, action[1:]))
        di["Date"] = action[0]
        if len(player_list_dict["actions"]) >= 1 :
            last = player_list_dict["actions"][-1].copy()
            last["Date"] = action[0]
            player_list_dict["actions"].append(last)
        player_list_dict["actions"].append(di)

    return json.dumps(player_list_dict, default=json_serial)

def detail(request, player_id) :
    player = get_object_or_404(Player, pk=player_id)
    register_form = ModifyUserForm(request.POST or None, instance= player.user)
    player_form = PlayerForm(request.POST or None, request.FILES or None, instance=player)

    if all((register_form.is_valid(), player_form.is_valid())):
        user_created = register_form.save()
        player = player_form.save(commit=False)
        player.user = user_created
        player.save()

        messages.success(request, (f"L'utilisateurs a bien été modifié !"))
        return redirect('game:detail', player_id)
    else :
        return render(request, 'game/detail.html', {'player' : player, 'register_form': register_form, 'player_form': player_form, 'player_json' : player.getJSON()})


# def delete(request, player_id) :
#     if request.user.is_authenticated :
#         player = get_object_or_404(Player, pk=player_id)
#         if request.user.id == player.user.id :
#             user = get_object_or_404(User, pk=player.user.id)
#             user.delete()
#             return HttpResponseRedirect(reverse('game:index'))
#         else :
#             messages.error(request, "Tu ne peux pas supprimer un autre joueur que toi petit malin")
#             return HttpResponseRedirect(reverse('game:index'))
#     else :
#         messages.error(request, "Il faut être connecté pour pouvoir supprimer un joueur")
#         return HttpResponseRedirect(reverse('game:index'))

def add_action(request) :
    if request.method == "POST" :
        form = ActionForm(request.POST, request.FILES)
        if form.is_valid() :
            form.save()
            messages.success(request, ("L'action a bien été ajoutée"))
            return redirect('game:add_action')
        else :
            messages.error(request, ("La valeur n'est pas valide"))
            return render(request, 'game/add_action.html', {'form':form})
    else :
        if request.user.is_authenticated :
            form = ActionForm(initial={'player': request.user.player.id})
        else :
            form = ActionForm()
        return render(request, 'game/add_action.html', {'form':form})

def mise(request) :
    mise_list = Mise.objects.all().order_by("fini", "-date_creation",)
    if request.method == "POST":
        if request.user.is_authenticated :
            nom = request.POST["miseNom"]
            if nom == None or nom.isspace() :
                messages.error(request, (f"Nom non valide pour la mise"))
                return redirect('game:mise')
            else :
                creator = get_object_or_404(Player, pk=request.user.player.id)

                mise = Mise(creator=creator, nom=nom, fini=False)
                mise.save()

                messages.success(request, (f"La mise {nom} a bien été ajouté !"))
                return redirect('game:mise_detail', mise_id=mise.id)
    else :
        return render(request, 'game/mise.html', {'mise_list':mise_list})
        
def mise_detail(request, mise_id) :
    mise = get_object_or_404(Mise, pk=mise_id)

    if request.method == "POST":
        if request.user.is_authenticated :
            val = Decimal(request.POST["miseValeur"])
            player_id = int(request.POST["id"])

            if val < 0 :
                messages.error(request, (f"La valeur ne peut pas être négative"))
                return redirect('game:mise_detail', mise_id=mise_id)

            if player_id in mise.player_id_list() :
                if val == 0 :
                    # Suppression de la miseJoueur
                    for miseJoueur in mise.misejoueur_set.all() :
                        if miseJoueur.player.id == player_id :
                            miseJoueur.delete()

                            messages.success(request, (f"La mise à bien été supprimée"))
                            return redirect('game:mise_detail', mise_id=mise_id)
                else :
                    # Modification de la mise
                    for miseJoueur in mise.misejoueur_set.all() :
                        if miseJoueur.player.id == player_id :
                            miseJoueur.mise_score = val
                            miseJoueur.save()

                            messages.success(request, (f"La valeur à bien été changé"))
                            return redirect('game:mise_detail', mise_id=mise_id)
            else :
                # Nouvelle misejoueur
                mise_joueur = MiseJoueur(player = get_object_or_404(Player, pk=player_id), mise=mise, mise_score=val)
                mise_joueur.save()

                messages.success(request, (f"La mise a bien été créée"))
                return redirect('game:mise_detail', mise_id=mise_id)
    
    return render(request, 'game/mise_detail.html', {'mise':mise})

def mise_delete(request, mise_id) :
    mise = get_object_or_404(Mise, pk=mise_id)

    if request.method == "POST" and request.user.is_authenticated :
        for miseJoueur in mise.misejoueur_set.all() :
            if f"check{miseJoueur.id}" in request.POST :
                miseJoueur.resultat = True
                miseJoueur.save()
        
        mise.fermer_mise()
        messages.success(request, (f"La mise a bien été fermée"))
        return redirect('game:mise')

    else :
        return render(request, 'game/mise_terminer.html', {'mise' : mise})

def score(request) :
    player_list = Player.objects.annotate(total_points=Sum('action__point')).order_by('-total_points')
    json_player_list = get_proper_JSON_from_player_list(player_list)
    date = datetime.now()
    return render(request, 'game/global_view_score.html', {'json_player_list' : json_player_list, 'date' : date, 'player_list':player_list})

def manoeuvre(request) :
    return render(request, 'game/manoeuvre.html')

def pari(request) :
    if request.method == 'POST' and request.user.is_superuser :
        pari_id = int(request.POST['id'])
        pari = get_object_or_404(Pari, pk=pari_id)
        res = int(request.POST['resultat'])
        if res in (1, 2) :
            pari.reussi = res
            pari.save()
            pari.termine_pari()
    list_pari = Pari.objects.order_by('reussi')
    return render(request, 'game/pari.html', {'liste_pari' : list_pari})