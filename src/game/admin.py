from django.contrib import admin

from .models import Player, Action, Mise, MiseJoueur, Pari, PariJoueur

class ActionInline(admin.StackedInline) :
    model = Action
    extra = 1

class PlayerAdmin(admin.ModelAdmin) :
    fields = ['user', 'description', 'photo']
    inlines = [ActionInline]

class ActionAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,               {'fields' : ['player']}),
        ('Information date', {'fields' : ['act_date']}),
        ('Valeurs',          {'fields' : ['point']}),
        ('Description',      {'fields' : ['description']})
    ]

class MiseJoueurAdmin(admin.ModelAdmin) :
    fieldsets = [
        ('Joueur',          {'fields' : ['player']}),
        ('Mise',            {'fields' : ['mise']}),
        ('Valeur de la mise du joueur', {'fields' : ['mise_score']})
    ]

class MiseJoueurInline(admin.StackedInline):
    model = MiseJoueur
    extra = 1

class MiseAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Createur',            {'fields' : ['creator']}),
        ('Nom',                 {'fields' : ['nom']}),
        ('Fini ?',              {'fields' : ['fini']})
    ]
    inlines = [MiseJoueurInline]

class PariJoueurAdmin(admin.ModelAdmin) :
    fieldsets = [
        ('Joueur',          {'fields' : ['player']}),
        ('Mise',            {'fields' : ['mise']}),
        ('Pari',            {'fields' : ['pari']})
    ]

class PariJoueurInline(admin.StackedInline):
        model = PariJoueur
        extra = 1

class PariAdmin(admin.ModelAdmin) :
    fieldsets = [
        ('Intitulé',        {'fields' : ['intitule']}),
        ('Cote',            {'fields' : ['cote']}),
        ('Reussi',          {'fields' : ['reussi']})
    ]
    inlines = [PariJoueurInline]

admin.site.register(Player, PlayerAdmin)
admin.site.register(Action, ActionAdmin)
admin.site.register(Mise, MiseAdmin)
admin.site.register(MiseJoueur, MiseJoueurAdmin)
admin.site.register(Pari, PariAdmin)
admin.site.register(PariJoueur, PariJoueurAdmin)