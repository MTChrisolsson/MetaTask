# home/views.py
from django.shortcuts import render
from django.http import HttpResponse

def index(request):
    return HttpResponse("<h1>Välkommen till Mediap.org (Home App)</h1><p>Du nådde domänen: " + request.get_host() + "</p>")