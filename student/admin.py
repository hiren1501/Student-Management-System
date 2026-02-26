from django.contrib import admin

from student.models import registrationstudent
from student.student_crud_models import StudentMarks
from student.fees_models import StudentFees

class StudentMarksAdmin(admin.ModelAdmin):
    list_display = ('student', 'subject', 'exam_type', 'marks_obtained', 'total_marks', 'percentage', 'faculty', 'date_recorded')
    list_filter = ('exam_type', 'subject', 'faculty', 'date_recorded')
    search_fields = ('student__name', 'subject', 'faculty__name')
    readonly_fields = ('date_recorded', 'percentage')
    
    def percentage(self, obj):
        return f"{obj.percentage:.2f}%"
    percentage.short_description = 'Percentage'

class StudentFeesAdmin(admin.ModelAdmin):
    list_display = ('get_grade_display_custom', 'fees', 'payment_method', 'updated_at')
    list_filter = ('payment_method', 'grade')
    search_fields = ('grade',)
    readonly_fields = ('created_at', 'updated_at')

# class registrationmodel(admin.ModelAdmin):
#     list_display=('fname','lname','email','phone','DOB','gender','course','address','password','cpassword')
# Register your models here.
admin.site.register(registrationstudent)
admin.site.register(StudentMarks, StudentMarksAdmin)
admin.site.register(StudentFees, StudentFeesAdmin)

