from django.db import models
from django import forms

class User(models.Model):
  username = models.CharField(max_length=200)

  def __str__(self) -> str:
    return self.username

class Result(models.Model):
  date = models.DateTimeField("results date")
  result = models.FloatField()
  user = models.ForeignKey(User, on_delete=models.CASCADE)

class GaussForm(forms.Form):
  def __init__(self, *args, **kwargs):
    numbers = kwargs.pop('numbers')
    super(GaussForm, self).__init__(*args, **kwargs)
    # for key,value in numbers:

