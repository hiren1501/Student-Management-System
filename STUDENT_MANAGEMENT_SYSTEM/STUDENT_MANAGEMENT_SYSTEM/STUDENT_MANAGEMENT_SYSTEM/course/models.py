from django.db import models

# Create your models here.
class courses(models.Model):
    subject_name=models.CharField(max_length=50)
    faculty_name=models.CharField(max_length=60,unique=True)
    subject_id=models.CharField(primary_key=True)