from django.forms import ModelForm
from django import forms
from .models import Student, Teacher, Guruh, GroupStudents

class StudentForm(ModelForm):
    class Meta:
        model = Student
        fields = "__all__"
        widgets = {
            'ism': forms.TextInput(attrs={'class': 'custom-class', 'placeholder': 'Ismni kiriting'},),
            'familiya': forms.TextInput(attrs={'class': 'custom-class', 'placeholder': 'Familiyani kiriting'},)
        }

class TeacherForm(ModelForm):
    class Meta:
        model = Teacher
        fields = "__all__"

class GuruhForm(ModelForm):
    class Meta:
        model = Guruh
        fields = "__all__"


class GroupStudentsForm(ModelForm):
    class Meta:
        model = GroupStudents
        fields = "__all__"
