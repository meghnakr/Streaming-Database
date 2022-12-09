from os import name
from django import forms

class MediaEditForm(forms.Form):
    name = forms.CharField(label='Media', max_length=100)
    media_type = forms.CharField(label='Media Type', max_length=100)
    age_rating = forms.CharField(label='Age Rating', max_length=100)
    year_of_release = forms.IntegerField(label='Year of Release')
    language = forms.CharField(label='Language', max_length=100)
    date_added = forms.DateField(label='Date Added')
    date_leaving = forms.DateField(label='Date Leaving')
    genre = forms.CharField(label='Genre', max_length=100)
    length_in_minutes = forms.IntegerField(label='Length in Minutes')
    company_id = forms.IntegerField(label='Company ID')
    #company_id = forms.IntegerField(label='company_id')
