from django.contrib import admin

from student.models import registrationstudent
# class registrationmodel(admin.ModelAdmin):
#     list_display=('fname','lname','email','phone','DOB','gender','course','address','password','cpassword')
# Register your models here.
admin.site.register(registrationstudent)
