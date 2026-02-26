from django.db import models
from student.fees_models import StudentFees

class registrationstudent(models.Model):
    first_name=models.CharField(max_length=50)
    last_name=models.CharField(max_length=50)
    email=models.EmailField(unique=True)
    phone=models.CharField(max_length=10)
    dob=models.DateField()
    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
    )
    gender = models.CharField(
        max_length=1, 
        choices=GENDER_CHOICES,  
    )
    # Course field kept for backward compatibility but not used for school
    COURSE_CHOICE=(
            ('bscit','BScIT'),
            ('bca','BCA'),
            ('msccs','MScCS'),
            ('mca','MCA'),
    )
    course=models.CharField(
        max_length=5,
        choices=COURSE_CHOICE,
        default="bca",
        blank=True,  # Make it optional
        null=True   # Allow null values
    )
    address=models.CharField(max_length=500)    
    password=models.CharField(max_length=10)
    confirmpassword=models.CharField(max_length=10)

# Create your models here.
