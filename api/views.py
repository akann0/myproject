from django.shortcuts import render
from django.http import HttpResponse
from ..polls.gsc import *

# Create your views here.

def index(request):
    return HttpResponse(scrape())