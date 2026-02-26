from django.db import models

class StudentFees(models.Model):
    GRADE_CHOICES = [
        (1, '1st Grade'),
        (2, '2nd Grade'),
        (3, '3rd Grade'),
        (4, '4th Grade'),
        (5, '5th Grade'),
        (6, '6th Grade'),
        (7, '7th Grade'),
        (8, '8th Grade'),
        (9, '9th Grade'),
        (10, '10th Grade'),
        (11, '11th Grade'),
        (12, '12th Grade'),
    ]
    
    PAYMENT_METHOD_CHOICES = [
        ('cash', 'Cash'),
        ('upi', 'UPI'),
        ('card', 'Debit/Credit Card'),
        ('bank_transfer', 'Bank Transfer'),
        ('cheque', 'Cheque'),
    ]
    
    grade = models.IntegerField(choices=GRADE_CHOICES, unique=True)
    fees = models.DecimalField(max_digits=10, decimal_places=2)
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHOD_CHOICES, default='cash')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Student Fee'
        verbose_name_plural = 'Student Fees'
        ordering = ['grade']
    
    def __str__(self):
        return f"Grade {self.grade} - ₹{self.fees}"
    
    def get_grade_display_custom(self):
        suffix = 'th'
        if self.grade == 1:
            suffix = 'st'
        elif self.grade == 2:
            suffix = 'nd'
        elif self.grade == 3:
            suffix = 'rd'
        return f"{self.grade}{suffix} Grade"
