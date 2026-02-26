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

#FACULTY CRUD VIEWS MUST BE IMPORTED OVER HERE:

#COURSE CRUD VIEWS MUST BE IMPORTED OVER HERE:

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',index1),
    path('login/',login_view,name="login"),
    path('register/',register,name="register"),
    path('admindashboard/',admindash,name="admin"),
    path('students/', student_list, name='student_list'),
    path('students/add/', student_create, name='student_create'),
    path('students/<int:pk>/edit/', student_update, name='student_update'),
    path('students/<int:pk>/delete/', student_delete, name='student_delete'),
    path('student/details/', student_detail, name='student_detail'),
]
