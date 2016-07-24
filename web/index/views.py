from django.shortcuts import render
from django.http import HttpResponse
from index.models import WebAnalyse

def index(request):
    now = time.strftime("%Y-%m-%d",time.localtime(time.time()))
    date = request.REQUEST.get("date",now)
    
