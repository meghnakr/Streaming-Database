from os import name
from django import forms

class MediaEditForm(forms.Form):
    name = forms.CharField(label='media', max_length=100)
    media_type = forms.CharField(label='media type', max_length=100)
    age_rating = forms.CharField(label='age rating', max_length=100)
    year_of_release = forms.IntegerField(label='year of release')
    language = forms.CharField(label='language', max_length=100)
    date_added = forms.DateField(label='date added')
    date_leaving = forms.DateField(label='date_leaving')
    genre = forms.CharField(label='genre', max_length=100)
    length_in_minutes = forms.IntegerField(label='length_in_minutes')
    #company_id = forms.IntegerField(label='company_id')
