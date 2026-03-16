from django.shortcuts import render
from .models import Course

def course_list(request):
    data = Course.objects.all()
    return render(request,"course_list.html",context={"courses": data})
