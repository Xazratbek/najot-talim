from django.shortcuts import render, redirect
from .models import Course

def course_list(request):
    data = Course.objects.all()
    return render(request,"course_list.html",context={"courses": data})

def add_course(request):
    if request.method == "POST":
        title = request.POST.get("title")
        instructor = request.POST.get("instructor")
        price = request.POST.get("price")

        Course.objects.create(title=title,instructor=instructor,price=price)

        return redirect("course-list")

    return render(request,"add-course.html")

def course_detail(request,id):
    crs = Course.objects.filter(id=id).first()

    return render(request,"course-detail.html",context={"crs": crs})

def update_course(request,id):
    crs = Course.objects.filter(id=id).first()
    if request.method == "POST":
        crs.title = request.POST.get("title")
        crs.instructor = request.POST.get("instructor")
        crs.price = request.POST.get("price")

        crs.save()

        return redirect("course-list")
    return render(request,"update-course.html",context={"crs": crs})

def delete_course(request,id):
    crs = Course.objects.filter(id=id).first()

    crs.delete()
    return redirect("course-list")