from django.contrib import admin
from .student_crud_models import Student

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ("name", "division", "semester", "rollnumber", "address")
    search_fields = ("name", "rollnumber", "division", "semester")
