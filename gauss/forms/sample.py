from django import forms

class SampleForm(forms.Form):
  numbers = forms.MultipleChoiceField()
