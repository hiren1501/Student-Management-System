from django.db import models
from student.student_crud_models import Grade

class faculties(models.Model):
    id = models.CharField(primary_key=True, max_length=20)
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=10, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    address = models.TextField(blank=True)
    qualification = models.CharField(max_length=100, blank=True)
    experience_years = models.IntegerField(default=0)
    grades = models.ManyToManyField(Grade, help_text="Select grades this faculty teaches")
    
    class Meta:
        verbose_name_plural = "Faculties"
        ordering = ['name']
    
    def __str__(self):
        return f"{self.name} (ID: {self.id})"