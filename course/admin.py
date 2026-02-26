from django.contrib import admin
from course.models import courses

# Register your models here.
class coursemodel(admin.ModelAdmin):
    list_display=('subject_id','subject_name','faculty_name')
    
def subject_id(self,obj):
    return obj.subject_id

admin.site.register(courses,coursemodel)