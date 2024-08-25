from django.urls import path
from . import views

app_name = "gauss"
urlpatterns = [
  path("", views.index, name="index"),
  path("sample", views.sample, name="sample")
  # path("rows", views.rows, name="rows"),
]
