from django.db import models
from django.utils import timezone

class User(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

    def get_total_point(self):
        return sum([action.point for action in self.action_set.all()])
    
class Action(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    point = models.IntegerField()
    act_date = models.DateTimeField('action date', default=timezone.now())

    def __str__(self):
        return str(self.user) + ' : ' + str(self.point)