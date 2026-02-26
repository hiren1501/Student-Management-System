from django.db import models
from student.student_crud_models import Grade, Stream

class Subject(models.Model):
    SUBJECT_CHOICES = [
        # Grades 1-10 subjects
        ('maths', 'Maths'),
        ('hindi', 'Hindi'),
        ('english', 'English'),
        ('social_science', 'Social Science'),
        ('general_science', 'General Science'),
        # Grade 11-12 Science subjects
        ('physics', 'Physics'),
        ('chemistry', 'Chemistry'),
        ('computer_science', 'Computer Science'),
        ('biology', 'Biology'),
        # Grade 11-12 Commerce subjects
        ('accountancy', 'Accountancy'),
        ('business_studies', 'Business Studies'),
        ('economics', 'Economics'),
        # Grade 11-12 Humanities subjects
        ('history', 'History'),
        ('political_science', 'Political Science'),
        ('painting', 'Painting'),
    ]
    
    code = models.CharField(max_length=10, unique=True, primary_key=True)
    name = models.CharField(max_length=100, choices=SUBJECT_CHOICES)
    grades = models.ManyToManyField(Grade)
    streams = models.ManyToManyField(Stream, blank=True)
    
    class Meta:
        ordering = ['name']
    
    def __str__(self):
        return f"{self.get_name_display()}"

class courses(models.Model):
    """Legacy model - keeping for backward compatibility"""
    subject_id = models.CharField(primary_key=True, max_length=10)
    subject_name = models.CharField(max_length=50)
    faculty_name = models.CharField(max_length=60, unique=True)
   