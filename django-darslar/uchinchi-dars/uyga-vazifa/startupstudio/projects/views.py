from django.shortcuts import render, redirect
from .models import Project

def project_list(request):
    projects = Project.objects.all()
    return render(request, "project_list.html", context={"projects": projects})

def project_details(request,id):
    one_pr = Project.objects.filter(id=id).first()
    return render(request,"project-detail.html",context={"pr": one_pr})

def add_project(request):
    if request.method == "POST":
        title = request.POST.get("title")
        description = request.POST.get("description")
        technology = request.POST.get("technology")
        client = request.POST.get("client")
        duration = request.POST.get("duration")
        completed = "completed" in request.POST

        Project.objects.create(title=title,description=description,technology=technology,client=client,duration=duration,completed=completed)

        return redirect("projects")

    return render(request,"add-project.html")

def update_project(request,id):
    pr = Project.objects.filter(id=id).first()

    if request.method == "POST":
        pr.title = request.POST.get("title")
        pr.description = request.POST.get("description")
        pr.technology = request.POST.get("technology")
        pr.client = request.POST.get("client")
        pr.duration = request.POST.get("duration")
        pr.completed = "completed" in request.POST

        pr.save()
        return redirect("projects")

    return render(request, "update-project.html", context={"pr": pr})

def delete_project(request, id):
    pr = Project.objects.get(id=id)
    pr.delete()

    return redirect("projects")