from django.db import models

class Student(models.Model):
    name = models.CharField(max_length=155,verbose_name="ism")
    age = models.IntegerField()
    phone_num = models.CharField(max_length=155)

    def __str__(self):
        return self.name
