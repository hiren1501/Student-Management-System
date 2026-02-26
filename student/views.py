from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from student.models import registrationstudent
from django.contrib import messages

@login_required
def student_edit_profile(request):
    """Allow students to edit their own profile/registration details"""
    try:
        student = registrationstudent.objects.get(email=request.user.email)
    except registrationstudent.DoesNotExist:
        messages.error(request, 'Student profile not found.')
        return redirect('index')
    
    if request.method == 'POST':
        # Update student details
        student.first_name = request.POST.get('first_name', student.first_name)
        student.last_name = request.POST.get('last_name', student.last_name)
        student.phone = request.POST.get('phone', student.phone)
        student.dob = request.POST.get('dob', student.dob)
        student.gender = request.POST.get('gender', student.gender)
        student.address = request.POST.get('address', student.address)
        
        try:
            student.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('student_welcome_page')
        except Exception as e:
            messages.error(request, f'Error updating profile: {str(e)}')
    
    context = {
        'student': student,
    }
    return render(request, 'student/student_edit_profile.html', context)


@login_required
def student_welcome_page(request):
    """Student dashboard/welcome page"""
    try:
        student = registrationstudent.objects.get(email=request.user.email)
    except registrationstudent.DoesNotExist:
        student = None
    return render(request, "student_welcome.html", {'student': student})
