from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

from decimal import *
from json import dumps
from datetime import date, datetime
from math import ceil

def json_serial(obj):
    """JSON serializer for objects not serializable by default json code"""

    if isinstance(obj, (datetime, date)):
        return obj.isoformat()
    if isinstance(obj, Decimal) :
        return str(obj)
    raise TypeError ("Type %s not serializable" % type(obj))


class Player(models.Model):
    photo = models.ImageField(upload_to='photo_de_profile/', null=True, blank=True)
    description = models.CharField(max_length=50, null=True, blank=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self) :
        return self.user.username
        
    def get_total_point(self) :
        return sum([action.point for action in self.action_set.all()])

    def getJSON(self) :
        player_dict = {'name' : self.user.username, 
                       'total_point' : self.get_total_point(),
                       'creation_date' : self.user.date_joined,
                       'actions' : []}
        tot = 0
        for action in self.action_set.all() :
            tot += action.point
            player_dict['actions'].append({'date_action' : action.act_date, 'score' : action.point, 'tot_score' : tot})

        return dumps(player_dict, default=json_serial)
    
class Action(models.Model):
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    point = models.DecimalField(max_digits=12, decimal_places=2)
    act_date = models.DateTimeField('action date', default=timezone.now)
    description = models.TextField(null= True)

    def __str__(self):
        return str(self.player) + ' : ' + str(self.point)

class Mise(models.Model) :
    date_creation = models.DateTimeField('date', default=timezone.now)
    creator = models.ForeignKey(Player, on_delete=models.PROTECT)
    fini = models.BooleanField(default=False)
    nom = models.CharField(max_length=50)

    def __str__(self) :
        return f"{self.nom} par {self.creator}"

    def user_id_list(self) :
        return [m.player.user.id for m in self.misejoueur_set.all()]
    
    def player_id_list(self) :
        return [m.player.id for m in self.misejoueur_set.all()]

    def mise_totale(self):
        return sum([m.mise_score for m in self.misejoueur_set.all()])
    
    def mise_totale_gagnant(self) :
        sum = 0
        for m in self.misejoueur_set.all() :
            if m.resultat :
                sum += m.mise_score
        return sum

    def fermer_mise(self) :
        self.fini = True
        self.save()
        for joueur in self.misejoueur_set.all() :
            joueur.fermeture_mise()

    def joueur_in_mise(self, player_pk) :
        return player_pk in self.misejoueur_set.all()

class MiseJoueur(models.Model) :
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    mise = models.ForeignKey(Mise, on_delete=models.CASCADE)
    mise_score = models.PositiveIntegerField()
    resultat = models.BooleanField(default=False)
    mise_date = models.DateTimeField('date', default=timezone.now)

    def __str__(self) :
        return str(self.player) + ' : ' + str(self.mise)
    
    def calcul_gain(self) :
        if self.resultat :
            proportion = self.mise_score / self.mise.mise_totale_gagnant()
            return ceil((self.mise.mise_totale() - self.mise.mise_totale_gagnant()) * proportion)
        else :
            return -self.mise_score

    def fermeture_mise(self) :
        action = Action(player=self.player, point=self.calcul_gain(), description=f"Gains de la mise {self.mise.nom}")
        action.save()

class Pari(models.Model) :
    intitule = models.CharField(max_length=200)
    cote = models.FloatField()
    reussi = models.IntegerField(default=0) #0 pas de réponse / 1 Réussi / 2 Raté

    def __str__(self) :
        return self.intitule + f" ({self.cote})";
    
    def fini(self) :
        return self.reussi != 0

    def termine_pari(self) :
        for pariJoueur in self.parijoueur_set.all() :
            pariJoueur.ajout_score()

class PariJoueur(models.Model) :
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    pari = models.ForeignKey(Pari, on_delete=models.CASCADE)
    mise = models.IntegerField()

    def fini(self) :
        return self.pari.fini()

    def gain_potentiel(self) :
        return self.pari.cote * self.mise

    def ajout_score(self) :
        if self.pari.reussi == 1 :
            action = Action(player=self.player, point=self.gain_potentiel(), description=f"Gains du pari {str(self.pari)}")
            action.save()