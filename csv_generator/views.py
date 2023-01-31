from django.shortcuts import render


def index(request):
    return render(request, "csv_generator/index.html")
