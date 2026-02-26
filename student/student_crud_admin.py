from django.contrib import admin
from .student_crud_models import Student

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ("name", "roll_number", "grade", "stream", "division")
    search_fields = ("name", "roll_number", "division")
