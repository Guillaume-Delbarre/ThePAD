from django import forms
from .models import Player, Action, MiseJoueur

class PlayerForm(forms.ModelForm) :
    # name = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nom du joueur'}))
    description = forms.CharField(max_length=200, required=False, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Description'}))
    photo = forms.ImageField(required=False, widget=forms.FileInput(attrs={'class': 'form-control'}))
    
    class Meta :
        model = Player
        fields = ('description', 'photo')

class ActionForm(forms.ModelForm) :
    player = forms.ModelChoiceField(queryset=Player.objects.all().order_by('user__username'), empty_label="Sélectionner un joueur", label='Joueur* :', widget=forms.Select(attrs={'class': 'form-select'}))
    point = forms.IntegerField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre de Points'}), label='Point* :')
    description = forms.CharField(required=False, widget=forms.Textarea(attrs={'class': 'form-control', 'rows': '5', 'placeholder': 'Précision sur l\'action'}), label='Description :')
    
    class Meta :
        model = Action
        fields = ('player', 'point', 'description')
