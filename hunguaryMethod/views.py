from django.shortcuts import render
from django.http import HttpRequest
from django.http import HttpResponse


# Create your views here.
def main(request):

    dictionary = {}

    return render(request, 'C:/Users/Andrey/PycharmProjects/djangoProject2/hunguaryMethod/templates/home.html', dictionary)
