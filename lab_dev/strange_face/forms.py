from django import forms
from .models import Person

class PersonAdd(forms.ModelForm):
    class Meta:
        model = Person
        fields = ['name','strange_value','normal_face','strange_face']

class PersonForm(forms.ModelForm):
    name = forms.CharField(
        label='名前',
        max_length=200,
        required=True,
        )

    normal_face = forms.ImageField(
        label='真顔の画像'
        )

    strange_face = forms.ImageField(
        label='変顔の画像'
        )

    class Meta:
        model = Person
        fields = ('name','normal_face','strange_face')
