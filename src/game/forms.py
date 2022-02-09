from django import forms
from .models import Player, Action

class PlayerForm(forms.ModelForm) :
    name = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nom du joueur'}))
    description = forms.CharField(max_length=200, required=False, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Description'}))
    photo = forms.ImageField(required=False, widget=forms.FileInput(attrs={'class': 'form-control'}))
    class Meta :
        model = Player
        fields = ('name', 'description', 'photo')

class ActionForm(forms.ModelForm) :
    player = forms.ModelChoiceField(queryset=Player.objects.all().order_by('name'), empty_label="Sélectionner un joueur", widget=forms.Select(attrs={'class': 'form-select'}))
    point = forms.IntegerField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre de Points'}))
    #act_date = forms.DateField(widget=forms.DateInput(attrs={'class': 'form-control', 'placeholder': 'Moment de l\'action'}))
    description = forms.CharField(required=False, widget=forms.Textarea(attrs={'class': 'form-control'}))
    class Meta :
        model = Action
        fields = ('player', 'point', 'description')