from django.contrib import admin
from .models import Student, Teacher, Guruh, GroupStudents

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ["id","ism","familiya","yosh"]
    list_filter = ["yosh"]
    ordering = ['-id']
    list_editable = ['ism']

@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    list_display = ["id","ism","familiya","yonalish"]
    list_filter = ["yonalish"]
    ordering = ["-id"]

@admin.register(Guruh)
class GuruhAdmin(admin.ModelAdmin):
    list_display = ["id","guruh_nomi","yonalish","boshlanish_sanasi"]
    ordering = ["-id"]

@admin.register(GroupStudents)
class GroupStudentsAdmin(admin.ModelAdmin):
    list_display = ["id","guruh","student"]
    ordering = ["-id"]