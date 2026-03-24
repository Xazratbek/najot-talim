from django.shortcuts import render, redirect
from .models import Flower

def flowers(request):
    flowers = Flower.objects.all()
    return render(request,"flowers_list.html",context={"flowers":flowers})

def add_flower(request):
    if request.method == "POST":
        name = request.POST.get("name")
        price = request.POST.get("price")
        color = request.POST.get("color")
        quantity = request.POST.get("quantity")
        description = request.POST.get("description")
        image = request.FILES.get("image")
        Flower.objects.create(name=name,price=price,color=color,quantity=quantity,description=description,image=image)

        return redirect("flowers_list")

    return render(request,"add-edit-flower.html")

def flower_detail(request,id):
    flower = Flower.objects.filter(id=id)

    return render(request,"flower_details.html",context={"flower": flower})

def update_flower(request,id):
    flower = Flower.objects.filter(id=id).first()
    if request.method == "POST":
        flower.name = request.POST.get("name")
        flower.price = request.POST.get("price")
        flower.color = request.POST.get("color")
        flower.quantity = request.POST.get("quantity")
        flower.description = request.POST.get("description")
        if request.FILES.get("image"):
            flower.image = request.FILES.get("image")

        flower.save()

        return redirect("flower-detail",flower.id)

    return render(request,"add-edit-flower.html",context={"flower": flower})

def delete_flower(request,id):
    flower = Flower.objects.get(id=id)
    flower.delete()
    return redirect("flowers_list")