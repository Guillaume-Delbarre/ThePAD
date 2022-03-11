from django import forms
from django.utils import timezone
from .models import Player, Action

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
    #act_date = forms.DateTimeField(widget=forms.TextInput(attrs={'type': 'datetime-local', 'class': 'form-control'}), label='Moment :', required=False)
    #act_date = forms.DateTimeField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'jj/mm/aaaa, hh:mm', 'title': 'jj/mm/aaaa, hh:mm'}), label='Moment :', required=False)
    description = forms.CharField(required=False, widget=forms.Textarea(attrs={'class': 'form-control', 'rows': '5', 'placeholder': 'Précision sur l\'action'}), label='Description :')
    class Meta :
        model = Action
        fields = ('player', 'point', 'description')