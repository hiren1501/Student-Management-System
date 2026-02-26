from django.db import models

# Create your models here.
class faculties(models.Model):
    name=models.CharField(max_length=60)
    email=models.EmailField(unique=True)
    id=models.CharField(primary_key=True)
    subject=models.CharField(max_length=100)