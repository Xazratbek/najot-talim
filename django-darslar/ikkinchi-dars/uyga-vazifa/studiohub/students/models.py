from django.db import models

class Student(models.Model):
    name = models.CharField(max_length=200)
    email = models.EmailField()
    age = models.IntegerField()
    joined_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name