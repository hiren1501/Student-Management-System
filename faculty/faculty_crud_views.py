from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import faculties
from student.student_crud_models import Grade
from django.contrib import messages

def is_admin(user):
    return user.is_staff

@login_required
@user_passes_test(is_admin)
def faculty_list(request):
    faculty_members = faculties.objects.all().prefetch_related('grades')
    return render(request, 'faculty/faculty_list.html', {'faculty_members': faculty_members})

@login_required
@user_passes_test(is_admin)
def faculty_create(request):
    grades = Grade.objects.all()
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        faculty_id = request.POST.get('id')
        phone = request.POST.get('phone', '')
        date_of_birth = request.POST.get('date_of_birth') or None
        address = request.POST.get('address', '')
        qualification = request.POST.get('qualification', '')
        experience_years = request.POST.get('experience_years', 0) or 0
        grade_ids = request.POST.getlist('grades')
        
        try:
            faculty = faculties.objects.create(
                name=name,
                email=email,
                id=faculty_id,
                phone=phone,
                date_of_birth=date_of_birth,
                address=address,
                qualification=qualification,
                experience_years=int(experience_years) if experience_years else 0
            )
            if grade_ids:
                faculty.grades.set(grade_ids)
            messages.success(request, 'Faculty created successfully!')
            return redirect('faculty_list')
        except Exception as e:
            messages.error(request, f'Error creating faculty: {str(e)}')
    
    return render(request, 'faculty/faculty_form.html', {'grades': grades})

@login_required
@user_passes_test(is_admin)
def faculty_update(request, pk):
    faculty = get_object_or_404(faculties, pk=pk)
    grades = Grade.objects.all()
    
    if request.method == 'POST':
        # Don't update the ID (primary key) - it's read-only
        faculty.name = request.POST.get('name')
        faculty.email = request.POST.get('email')
        faculty.phone = request.POST.get('phone', '')
        faculty.date_of_birth = request.POST.get('date_of_birth') or None
        faculty.address = request.POST.get('address', '')
        faculty.qualification = request.POST.get('qualification', '')
        experience_years = request.POST.get('experience_years', 0) or 0
        faculty.experience_years = int(experience_years) if experience_years else 0
        
        grade_ids = request.POST.getlist('grades')
        if grade_ids:
            faculty.grades.set(grade_ids)
        else:
            faculty.grades.clear()
        
        try:
            faculty.save()
            messages.success(request, 'Faculty updated successfully!')
            return redirect('faculty_list')
        except Exception as e:
            messages.error(request, f'Error updating faculty: {str(e)}')
    
    return render(request, 'faculty/faculty_form.html', {'faculty': faculty, 'grades': grades})

@login_required
@user_passes_test(is_admin)
def faculty_delete(request, pk):
    faculty = get_object_or_404(faculties, pk=pk)
    if request.method == 'POST':
        faculty.delete()
        messages.success(request, 'Faculty deleted successfully!')
        return redirect('faculty_list')
    return render(request, 'faculty/faculty_confirm_delete.html', {'faculty': faculty})

@login_required
def faculty_detail(request, pk):
    faculty = get_object_or_404(faculties, pk=pk)
    return render(request, 'faculty/faculty_detail.html', {'faculty': faculty})
