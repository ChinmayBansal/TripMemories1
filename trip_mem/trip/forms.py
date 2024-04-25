# trips/forms.py
from django import forms
from .models import Trip, Review
from django.db.models.functions import ExtractYear
from django.db.models import Count

class TripForm(forms.ModelForm):
    class Meta:
        model = Trip
        fields = ['destination', 'description', 'start_date', 'end_date']
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'end_date': forms.DateInput(attrs={'type': 'date'}),
        }
class TripYearFilterForm(forms.Form):
    year = forms.ChoiceField(choices=[], required=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        years = Trip.objects.annotate(year=ExtractYear('start_date')).values('year').distinct().order_by('-year')
        year_choices = [(str(year['year']), str(year['year'])) for year in years]
        if not year_choices:
            self.fields['year'].choices = [('', 'No trips to filter')]
        else:
            self.fields['year'].choices = [('', 'All')] + year_choices



class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['text', 'rating'] 
        widgets = {
            'date_posted': forms.DateInput(attrs={'type': 'date'}),
            'rating': forms.NumberInput(attrs={'min': 1, 'max': 5})  #if rating is between 1 and 5
        }
