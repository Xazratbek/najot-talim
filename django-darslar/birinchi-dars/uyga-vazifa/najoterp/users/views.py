from django.shortcuts import render
from django.http import HttpResponse
from .models import Student

def get_students(request):
    students = Student.objects.all()
    print(students)
    return HttpResponse(f"Studentlar: {[student.name for student in students]}")

def get_student_by_id(request,student_id):
    students = Student.objects.filter(id=student_id)
    print(students)
    return HttpResponse(f"Student: {students[0].name} {students[0].age} {students[0].phone_num}")