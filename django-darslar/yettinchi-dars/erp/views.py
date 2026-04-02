from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from .forms import *
from .models import *

class StudentCreateView(View):
    def get(self, request):
        form = StudentForm()
        return render(request,"student/create.html",context={"form": form})

    def post(self, request):
        form = StudentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("student-list")
        return render(request,"student/create.html",context={"form": form})

class StudentListView(View):
    def get(self, request):
        students = Student.objects.all()
        return render(request,"student/list.html",context={"students": students})

class StudentUpdateView(View):
    def get(self, request, pk):
        student = get_object_or_404(Student, pk=pk)
        form = StudentForm(instance=student)
        return render(request, "student/update.html",context={"form":form,"student":student})

    def post(self, request, pk):
        student = get_object_or_404(Student, pk=pk)
        form = StudentForm(request.POST,instance=student)
        if form.is_valid():
            form.save()
            return redirect("student-list")

        return render(request, "student/update.html",context={"form":form,"student":student})

class StudentDetailView(View):
    def get(self, request, pk):
        student = get_object_or_404(Student, pk=pk)
        return render(request, "student/detail.html",context={"student": student})

class StudentDeleteView(View):
    def get(self, request, pk):
        student = get_object_or_404(Student, pk=pk)
        return render(request, "student/delete.html",context={"student":student})

    def post(self, request, pk):
        student = get_object_or_404(Student, pk=pk)
        student.delete()
        return redirect("student-list")

########## Teacher Viewlari

class TeacherCreateView(View):
    def get(self, request):
        form = TeacherForm()
        return render(request,"teacher/create.html",context={"form": form})

    def post(self, request):
        form = TeacherForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("teacher-list")
        return render(request,"teacher/create.html",context={"form": form})

class TeacherListView(View):
    def get(self, request):
        teachers = Teacher.objects.all()
        return render(request,"teacher/list.html",context={"teachers": teachers})

class TeacherUpdateView(View):
    def get(self, request, pk):
        teacher = get_object_or_404(Teacher, pk=pk)
        form = TeacherForm(instance=teacher)
        return render(request, "teacher/update.html",context={"form":form,"teacher":teacher})

    def post(self, request, pk):
        teacher = get_object_or_404(Teacher, pk=pk)
        form = TeacherForm(request.POST,instance=teacher)
        if form.is_valid():
            form.save()
            return redirect("teacher-list")

        return render(request, "teacher/update.html",context={"form":form,"teacher":teacher})

class TeacherDetailView(View):
    def get(self, request, pk):
        teacher = get_object_or_404(Teacher, pk=pk)
        teacher_groups = Guruh.objects.filter(oqituvchi__pk=teacher.pk)
        return render(request, "teacher/detail.html",context={"teacher": teacher,"teacher_groups": teacher_groups})

class TeacherDeleteView(View):
    def get(self, request, pk):
        teacher = get_object_or_404(Teacher, pk=pk)
        return render(request, "teacher/delete.html",context={"teacher":teacher})

    def post(self, request, pk):
        teacher = get_object_or_404(Teacher, pk=pk)
        teacher.delete()
        return redirect("teacher-list")

######## Guruh Viewlari
class GuruhCreateView(View):
    def get(self, request):
        form = GuruhForm()
        return render(request,"guruh/create.html",context={"form": form})

    def post(self, request):
        form = GuruhForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("guruh-list")
        return render(request,"guruh/create.html",context={"form": form})

class GuruhListView(View):
    def get(self, request):
        guruhlar = Guruh.objects.all().select_related("oqituvchi")
        return render(request,"guruh/list.html",context={"guruhlar": guruhlar})

class GuruhUpdateView(View):
    def get(self, request, pk):
        guruh = get_object_or_404(Guruh, pk=pk)
        form = GuruhForm(instance=guruh)
        return render(request, "guruh/update.html",context={"form":form,"guruh":guruh})

    def post(self, request, pk):
        guruh = get_object_or_404(Guruh, pk=pk)
        form = GuruhForm(request.POST,instance=guruh)
        if form.is_valid():
            form.save()
            return redirect("guruh-list")

        return render(request, "guruh/update.html",context={"form":form,"guruh":guruh})

class GuruhDetailView(View):
    def get(self, request, pk):
        guruh = get_object_or_404(Guruh, pk=pk)
        group_students = GroupStudents.objects.filter(guruh__guruh_nomi__icontains=guruh.guruh_nomi).select_related("guruh","student")
        print(len(group_students))
        return render(request, "guruh/detail.html",context={"guruh": guruh,"group_students": group_students})

class GuruhDeleteView(View):
    def get(self, request, pk):
        guruh = get_object_or_404(Guruh, pk=pk)
        return render(request, "guruh/delete.html",context={"guruh":guruh})

    def post(self, request, pk):
        guruh = get_object_or_404(Guruh, pk=pk)
        guruh.delete()
        return redirect("guruh-list")