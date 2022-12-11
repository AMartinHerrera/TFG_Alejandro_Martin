# In this file you add the forms that you application need to use

from django import forms
from .models import Player

class PlayerInputForm(forms.Form):

    player = forms.CharField()