import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'STUDENT_MANAGEMENT_SYSTEM.settings')
django.setup()

from student.student_crud_models import Student

print("Student model fields:")
for field in Student._meta.fields:
    print(f"  - {field.name}: {field.get_internal_type()}")
