from django import forms
from .models import Conference
class ConferenceModel(forms.ModelForm):
    class Meta:
        model=Conference
        fields=['name','theme','description','location','start_date','end_date']
        labels= {
            'name':"nom de la conference",
            'theme':"Thematiques",
            'desc':"Description",
            'location':"Location",
            'start_date':"Date debut de la conference",
            'end_date':"Date fin de la conference"
        }
        widgets ={
            'name': forms.TextInput(
            attrs={
                'placeholder' :"Ex - Conference"
            }
            ),
            'start_date' : forms.DateInput(
            attrs={
                'type':'date',
                'placeholder':"date de debut"
            }
            ),
            'end_date' : forms.DateInput(
            attrs={
                'type':'date',
                'placeholder':"date de fin"
            }
            )
        }