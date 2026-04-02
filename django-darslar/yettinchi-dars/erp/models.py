from django.db import models

class YonalishChoice(models.TextChoices):
    BACKEND = "backend", "BACKEND"
    FRONTEND = "frontend", "FRONTEND"
    MOBILE = "mobile", "MOBILE"

class Student(models.Model):
    ism = models.CharField(max_length=100,verbose_name="Ism")
    familiya = models.CharField(max_length=100,verbose_name="Familiya",help_text="Familiyani kiriting",error_messages="Iltimos familiyani tog'ri kiriting")
    yosh = models.IntegerField()
    phone = models.CharField(max_length=15)

    def __str__(self):
        return self.ism

    class Meta:
        db_table = "student"
        verbose_name = "Student"
        verbose_name_plural = "Studentlar"


class Teacher(models.Model):
    ism = models.CharField(max_length=150)
    familiya = models.CharField(max_length=150)
    yonalish = models.CharField(max_length=150,choices=YonalishChoice.choices, default=YonalishChoice.BACKEND)
    staj = models.IntegerField(default=0)

    def __str__(self):
        return self.ism

    class Meta:
        db_table = "teacher"
        verbose_name = "Teacher"
        verbose_name_plural = "Teacherlar"

class Guruh(models.Model):
    guruh_nomi = models.CharField(max_length=150,verbose_name="Guruh nomi")
    yonalish = models.CharField(max_length=50,choices=YonalishChoice.choices,default=YonalishChoice.BACKEND)
    boshlanish_sanasi = models.DateField(verbose_name="Boshlanish sanasi")
    tugash_sanasi = models.DateField(verbose_name="Tugash sanasi")
    oqituvchi = models.ForeignKey(Teacher,on_delete=models.RESTRICT)

    def __str__(self):
        return f"GURUH: {self.guruh_nomi} | O'qituvchi: {self.oqituvchi}"

    class Meta:
        db_table = "guruh"
        verbose_name = "Guruh"
        verbose_name_plural = "Guruhlar"

class GroupStudents(models.Model):
    guruh = models.ForeignKey(Guruh,on_delete=models.RESTRICT)
    student = models.ForeignKey(Student,on_delete=models.RESTRICT)

    def __str__(self):
        return f"{self.guruh.guruh_nomi} | {self.student.ism}"