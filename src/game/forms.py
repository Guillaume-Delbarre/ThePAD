from django import forms
from .models import Player

class PlayerForm(forms.ModelForm) :
    name = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nom du joueur'}))
    description = forms.CharField(max_length=200, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Description'}))
    photo = forms.ImageField(widget=forms.FileInput(attrs={'class': 'form-control'}))
    class Meta :
        model = Player
        fields = ('name', 'description', 'photo')