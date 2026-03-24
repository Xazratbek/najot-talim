from django.shortcuts import render, redirect
from .models import Laptop


def laptop_list(request):
    laptops = Laptop.objects.all()
    return render(request, "laptops-list.html",context={"laptops": laptops})

def add_laptop(request):
    if request.method == "POST":
        print(request.POST)
        brand = request.POST.get("brand")
        name = request.POST.get("name")
        description = request.POST.get("description")
        price = request.POST.get("price")
        cpu = request.POST.get("cpu")
        gpu = request.POST.get("gpu")
        ram = request.POST.get("ram")
        storage = request.POST.get("storage")
        storage_type = request.POST.get("storage_type")
        screen_size = request.POST.get("screen_size")
        resolution = request.POST.get("resolution")
        battery = request.POST.get("battery")
        weight = request.POST.get("weight")
        os = request.POST.get("os")
        image = request.FILES.get("image")

        Laptop.objects.create(
            brand=brand, name=name, description=description, price=price,
            cpu=cpu, gpu=gpu, storage=storage, storage_type=storage_type,
            ram=ram, screen_size=screen_size, resolution=resolution,
            battery=battery, weight=weight, os=os, image=image
        )

        return redirect("laptop-list")

    return render(request, "add-edit-laptop.html")

def laptop_detail(request, id):
    laptop = Laptop.objects.filter(id=id)

    return render(request,"laptop-detail.html",context={"laptop": laptop})

def update_laptop(request,id):
    laptop = Laptop.objects.filter(id=id).first()

    if request.method == "POST":
        laptop.brand = request.POST.get("brand")
        laptop.name = request.POST.get("name")
        laptop.description = request.POST.get("description")
        laptop.price = request.POST.get("price")
        laptop.cpu = request.POST.get("cpu")
        laptop.gpu = request.POST.get("gpu")
        laptop.ram = request.POST.get("ram")
        laptop.storage = request.POST.get("storage")
        laptop.storage_type = request.POST.get("storage_type")
        laptop.screen_size = request.POST.get("screen_size")
        laptop.resolution = request.POST.get("resolution")
        laptop.battery = request.POST.get("battery")
        laptop.weight = request.POST.get("weight")
        laptop.os = request.POST.get("os")

        if request.FILES.get("image"):
            laptop.image = request.FILES.get("image")

        laptop.save()

        return redirect("laptop-detail", laptop.id)

    return render(request, "add-edit-laptop.html", {"laptop": [laptop] if laptop else None})