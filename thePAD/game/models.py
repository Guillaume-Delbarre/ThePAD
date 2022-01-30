from django.db import models

class User(models.Model) :
    nom = models.CharField(max_length=50)
    
class Action(models.Model) :
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    points = models.IntegerField()
    act_date = models.TimeField('action date')