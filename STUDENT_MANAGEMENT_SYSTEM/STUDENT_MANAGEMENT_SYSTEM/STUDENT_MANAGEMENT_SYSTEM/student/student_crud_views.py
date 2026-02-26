from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from .student_crud_models import Student
from django.contrib import messages

def is_admin(user):
    return user.is_staff

# Admin CRUD views
@login_required
@user_passes_test(is_admin)
def student_list(request):
    students = Student.objects.all()
    return render(request, 'student/student_list.html', {'students': students})

@login_required
@user_passes_test(is_admin)
def student_create(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        division = request.POST.get('division')
        semester = request.POST.get('semester')
        rollnumber = request.POST.get('rollnumber')
        address = request.POST.get('address')
        Student.objects.create(name=name, division=division, semester=semester, rollnumber=rollnumber, address=address)
        messages.success(request, 'Student created successfully!')
        return redirect('student_list')
    return render(request, 'student/student_form.html')

@login_required
@user_passes_test(is_admin)
def student_update(request, pk):
    student = get_object_or_404(Student, pk=pk)
    if request.method == 'POST':
        student.name = request.POST.get('name')
        student.division = request.POST.get('division')
        student.semester = request.POST.get('semester')
        student.rollnumber = request.POST.get('rollnumber')
        student.address = request.POST.get('address')
        student.save()
        messages.success(request, 'Student updated successfully!')
        return redirect('student_list')
    return render(request, 'student/student_form.html', {'student': student})

@login_required
@user_passes_test(is_admin)
def student_delete(request, pk):
    student = get_object_or_404(Student, pk=pk)
    if request.method == 'POST':
        student.delete()
        messages.success(request, 'Student deleted successfully!')
        return redirect('student_list')
    return render(request, 'student/student_confirm_delete.html', {'student': student})

# Student detail view (students can only view their own details)
@login_required
def student_detail(request):
    # Assuming student's rollnumber is stored in user.username after login
    try:
        student = Student.objects.get(rollnumber=request.user.username)
    except Student.DoesNotExist:
        student = None
    return render(request, 'student/student_detail.html', {'student': student})
