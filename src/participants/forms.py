from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import User
from django import forms

class RegisterUserForm(UserCreationForm) :

    class Meta :
        model = User
        fields = ('username', 'password1', 'password2', )

    def __init__(self, *args, **kwargs) :
        super(RegisterUserForm, self).__init__(*args, **kwargs)

        self.fields['username'].widget.attrs['class'] = 'form-control'
        self.fields['password1'].widget.attrs['class'] = 'form-control'
        self.fields['password2'].widget.attrs['class'] = 'form-control'

class ModifyUserForm(forms.ModelForm):

    username = forms.CharField(max_length=150, widget=forms.TextInput(attrs={'class': 'form-control'}), label='Nom d\'utilisateur')

    class Meta:
        model = User
        fields = ['username', ]