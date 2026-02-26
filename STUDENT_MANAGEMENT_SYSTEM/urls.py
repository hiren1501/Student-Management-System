"""
URL configuration for STUDENT_MANAGEMENT_SYSTEM project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from STUDENT_MANAGEMENT_SYSTEM.views import *
# Student CRUD views
from student.student_crud_views import (
    student_list, student_create, student_update, student_delete, student_detail
)
from student.student_crud_views import (
    attendance_list, attendance_mark
)
from student.marks_views import (
    marks_list, marks_add, marks_edit, marks_delete, marks_download, marks_email, marks_upload
)
from student.marks_views import test_email
# Student profile views
from student.views import (
    student_edit_profile, student_welcome_page
)
# Student fees views
from student.fees_views import (
    student_fees_list, student_fees_update, student_fees_delete
)


# Faculty CRUD views
from faculty.faculty_crud_views import (
    faculty_list, faculty_create, faculty_update, faculty_delete, faculty_detail
)

#COURSE CRUD VIEWS MUST BE IMPORTED OVER HERE:

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',index1),
    path('timetable/',timetable_view,name="timetable"),
    path('login/',login_view,name="login"),
    path('register/',register,name="register"),
    path('admindashboard/',admindash,name="admin"),
    path('faculty-welcome/', faculty_welcome, name='faculty_welcome'),
    path('students/', student_list, name='student_list'),
    path('students/add/', student_create, name='student_create'),
    path('students/<int:pk>/edit/', student_update, name='student_update'),
    path('students/<int:pk>/delete/', student_delete, name='student_delete'),
    path('students/<int:pk>/', student_detail, name='student_detail'),
    path('student/details/', student_detail, name='student_detail_own'),
    path('student/welcome/', student_welcome_page, name='student_welcome_page'),
    path('student/edit-profile/', student_edit_profile, name='student_edit_profile'),
    path('attendance/', attendance_list, name='attendance_list'),
    path('attendance/mark/', attendance_mark, name='attendance_mark'),
    path('marks/', marks_list, name='marks_list'),
    path('marks/add/', marks_add, name='marks_add'),
    path('marks/upload/', marks_upload, name='marks_upload'),
    path('marks/<int:pk>/edit/', marks_edit, name='marks_edit'),
    path('marks/<int:pk>/delete/', marks_delete, name='marks_delete'),
    path('marks/<int:pk>/download/', marks_download, name='marks_download'),
    path('marks/<int:pk>/email/', marks_email, name='marks_email'),
    path('email-test/', test_email, name='email_test'),
    path('course/add/', course_add, name='course_add'),
    path('course/view/', course_view, name='course_view'),
    path('course/<int:subject_id>/edit/', course_update, name='course_update'),
    path('course/<int:subject_id>/delete/', course_delete, name='course_delete'),
    # Faculty CRUD URLs
    path('faculty/', faculty_list, name='faculty_list'),
    path('faculty/add/', faculty_create, name='faculty_create'),
    path('faculty/<str:pk>/edit/', faculty_update, name='faculty_update'),
    path('faculty/<str:pk>/delete/', faculty_delete, name='faculty_delete'),
    path('faculty/<str:pk>/', faculty_detail, name='faculty_detail'),
    # Student Fees URLs
    path('student_fees/', student_fees_list, name='student_fees_list'),
    path('student_fees/<int:pk>/update/', student_fees_update, name='student_fees_update'),
    path('student_fees/<int:pk>/delete/', student_fees_delete, name='student_fees_delete'),
]
