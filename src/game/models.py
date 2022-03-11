from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

class Player(models.Model):
    photo = models.ImageField(upload_to='photo_de_profile/', null=True, blank=True)
    description = models.CharField(max_length=200, null=True, blank=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)

    def __str__(self):
        return self.user.username
        
    def get_total_point(self):
        return sum([action.point for action in self.action_set.all()])
    
class Action(models.Model):
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    point = models.IntegerField()
    act_date = models.DateTimeField('action date', default=timezone.now())
    description = models.TextField(null= True)

    def __str__(self):
        return str(self.user) + ' : ' + str(self.point)