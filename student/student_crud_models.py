from django.db import models
from django.utils import timezone

class Grade(models.Model):
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
    grade = models.IntegerField(choices=GRADE_CHOICES, unique=True)
    
    def __str__(self):
        return f"{self.get_grade_display()}"

class Stream(models.Model):
    STREAM_CHOICES = [
        ('science', 'Science'),
        ('commerce', 'Commerce'),
        ('humanities', 'Humanities'),
    ]
    name = models.CharField(max_length=50, choices=STREAM_CHOICES, unique=True)
    grades = models.ManyToManyField(Grade, limit_choices_to={'grade__gte': 11})
    
    def __str__(self):
        return self.get_name_display()

class Student(models.Model):
    name = models.CharField(max_length=100)
    roll_number = models.CharField(max_length=20, unique=True)
    grade = models.ForeignKey(Grade, on_delete=models.CASCADE)
    stream = models.ForeignKey(Stream, on_delete=models.SET_NULL, null=True, blank=True)
    division = models.CharField(max_length=10, help_text="e.g., A, B, C")
    address = models.TextField()
    phone = models.CharField(max_length=10, blank=True)
    email = models.EmailField(blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['grade', 'division', 'name']

    def __str__(self):
        if self.stream:
            return f"{self.name} ({self.roll_number}) - Grade {self.grade.grade} {self.stream.get_name_display()}"
        return f"{self.name} ({self.roll_number}) - Grade {self.grade.grade}"


class Attendance(models.Model):
    """Represents an attendance session for a particular grade (and optional stream) on a date."""
    date = models.DateField()
    grade = models.ForeignKey(Grade, on_delete=models.CASCADE)
    # stream is optional (for grades 1-10 it will be null)
    stream = models.ForeignKey('Stream', on_delete=models.CASCADE, null=True, blank=True)

    class Meta:
        unique_together = ('date', 'grade', 'stream')
        ordering = ['-date']

    def __str__(self):
        if self.stream:
            return f"Attendance {self.date} - Grade {self.grade.grade} {self.stream.get_name_display()}"
        return f"Attendance {self.date} - Grade {self.grade.grade}"


class AttendanceRecord(models.Model):
    attendance = models.ForeignKey(Attendance, on_delete=models.CASCADE, related_name='records')
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    present = models.BooleanField(default=False)

    class Meta:
        unique_together = ('attendance', 'student')

    def __str__(self):
        return f"{self.student} - {'Present' if self.present else 'Absent'} on {self.attendance.date}"


class StudentMarks(models.Model):
    EXAM_TYPE_CHOICES = [
        ('midterm', 'Mid-Term'),
        ('final', 'Final'),
        ('quiz', 'Quiz'),
        ('assignment', 'Assignment'),
        ('project', 'Project'),
    ]
    
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='marks')
    subject = models.CharField(max_length=100)
    exam_type = models.CharField(max_length=20, choices=EXAM_TYPE_CHOICES)
    marks_obtained = models.FloatField()
    total_marks = models.FloatField(default=100)
    faculty = models.ForeignKey('faculty.faculties', on_delete=models.SET_NULL, null=True, blank=True)
    date_recorded = models.DateTimeField(default=timezone.now)
    
    class Meta:
        ordering = ['-date_recorded']
        unique_together = ('student', 'subject', 'exam_type')
    
    def __str__(self):
        percentage = (self.marks_obtained / self.total_marks) * 100 if self.total_marks > 0 else 0
        return f"{self.student.name} - {self.subject} ({self.exam_type}): {self.marks_obtained}/{self.total_marks}"
    
    @property
    def percentage(self):
        return (self.marks_obtained / self.total_marks) * 100 if self.total_marks > 0 else 0
