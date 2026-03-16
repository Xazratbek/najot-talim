from django.shortcuts import render
from .models import StartupIdea

def startups(request):
    data = StartupIdea.objects.all()
    return render(request,"startup_list.html",context={"startups": data})