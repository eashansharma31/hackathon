from django import forms
FRUIT_CHOICES= [
    ('Good', 'Good'),
    ('Bad', 'Bad'),
    ('Best', 'Best'),
   
    ]

class UserForm(forms.Form):
   
    fav= forms.CharField(widget=forms.RadioSelect(choices=FRUIT_CHOICES))