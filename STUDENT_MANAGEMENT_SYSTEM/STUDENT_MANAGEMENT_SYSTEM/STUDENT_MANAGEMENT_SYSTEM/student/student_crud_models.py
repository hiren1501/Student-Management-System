from django.db import models

class Student(models.Model):
    name = models.CharField(max_length=100)
    division = models.CharField(max_length=10)
    semester = models.IntegerField()
    rollnumber = models.CharField(max_length=20, unique=True)
    address = models.TextField()

    def __str__(self):
        return f"{self.name} ({self.rollnumber})"
