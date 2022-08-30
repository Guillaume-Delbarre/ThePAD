from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

from json import dumps
from datetime import date, datetime

def json_serial(obj):
    """JSON serializer for objects not serializable by default json code"""

    if isinstance(obj, (datetime, date)):
        return obj.isoformat()
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
    point = models.IntegerField()
    act_date = models.DateTimeField('action date', default=timezone.now)
    description = models.TextField(null= True)

    def __str__(self):
        return str(self.player) + ' : ' + str(self.point)