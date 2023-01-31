from django.contrib import admin
from django.urls import path, include

from csv_generator.views import index

urlpatterns = [
    path("", index, name="index",)
]

app_name = "csv_generator"
