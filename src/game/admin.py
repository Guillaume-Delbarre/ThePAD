from django.contrib import admin

from .models import Player, Action

class ActionInline(admin.StackedInline) :
    model = Action
    extra = 1

class PlayerAdmin(admin.ModelAdmin) :
    fields = ['user', 'name', 'description', 'photo']
    inlines = [ActionInline]

class ActionAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,               {'fields' : ['player']}),
        ('Information date', {'fields' : ['act_date']}),
        ('Valeurs',          {'fields' : ['point']})
    ]

admin.site.register(Player, PlayerAdmin)
admin.site.register(Action, ActionAdmin)