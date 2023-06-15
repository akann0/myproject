from django.http import HttpResponse
#import render
from django.shortcuts import render
from .game import *
from .gsc import *


def index(request):
    return HttpResponse(scrape())
    # context = {
    #     'game': play_game(),
    # }
    # return render(request, 'index.html', context=context)

def detail(request, question_id):
    return HttpResponse("You're looking at question %s." % question_id)

def results(request, question_id):
    response = "You're looking at the results of question %s."
    return HttpResponse(response % question_id)

def vote(request, question_id):
    return HttpResponse("You're voting on question %s." % question_id)

