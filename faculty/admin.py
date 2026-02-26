
from django.contrib import admin
from .models import faculties

class FacultiesAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'email', 'phone', 'experience_years', 'display_grades')
    list_filter = ('experience_years', 'grades')
    search_fields = ('name', 'email', 'id')
    filter_horizontal = ('grades',)  # Makes it easier to assign multiple grades
    fieldsets = (
        ('Basic Information', {
            'fields': ('id', 'name', 'email', 'phone')
        }),
        ('Personal Details', {
            'fields': ('date_of_birth', 'address')
        }),
        ('Professional Information', {
            'fields': ('qualification', 'experience_years', 'grades')
        }),
    )
    
    def display_grades(self, obj):
        """Display assigned grades in the list view"""
        grades = obj.grades.all()
        if grades:
            return ', '.join([g.get_grade_display() for g in grades])
        return 'No grades assigned'
    display_grades.short_description = 'Assigned Grades'

admin.site.register(faculties, FacultiesAdmin)

