from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from .student_crud_models import Student, Grade, Stream
from django.contrib import messages
from django.shortcuts import render
from django.utils import timezone
from django.core.mail import send_mail
from django.conf import settings
from .student_crud_models import Student, Attendance, AttendanceRecord, Grade, Stream

def is_admin(user):
    return user.is_staff

# Admin CRUD views
@login_required
@user_passes_test(is_admin)
def student_list(request):
    students = Student.objects.all()
    grades = Grade.objects.all()
    selected_grade = request.GET.get('grade')
    
    if selected_grade:
        students = students.filter(grade_id=selected_grade)
    
    context = {
        'students': students,
        'grades': grades,
        'selected_grade': selected_grade,
    }
    return render(request, 'student/student_list.html', context)

@login_required
@user_passes_test(is_admin)
def student_create(request):
    grades = Grade.objects.all()
    streams = Stream.objects.all()
    
    # Ensure Stream objects exist
    if streams.count() == 0:
        Stream.objects.get_or_create(name='science')
        Stream.objects.get_or_create(name='commerce')
        Stream.objects.get_or_create(name='humanities')
        streams = Stream.objects.all()
    
    if request.method == 'POST':
        name = request.POST.get('name')
        roll_number = request.POST.get('roll_number')
        grade_id = request.POST.get('grade')
        stream_id = request.POST.get('stream')
        division = request.POST.get('division')
        address = request.POST.get('address')
        phone = request.POST.get('phone')
        email = request.POST.get('email')
        date_of_birth = request.POST.get('date_of_birth') or None
        
        try:
            grade = Grade.objects.get(id=grade_id)
            stream = None
            if stream_id:
                try:
                    # Try to get by ID first
                    stream = Stream.objects.get(id=stream_id)
                except (Stream.DoesNotExist, ValueError):
                    # If ID lookup fails, try by name (for fallback hardcoded values)
                    try:
                        stream = Stream.objects.get(name=stream_id)
                    except Stream.DoesNotExist:
                        pass
            
            student = Student.objects.create(
                name=name,
                roll_number=roll_number,
                grade=grade,
                stream=stream,
                division=division,
                address=address,
                phone=phone,
                email=email,
                date_of_birth=date_of_birth
            )
            
            # Send welcome email to the student
            if email:
                try:
                    send_mail(
                        subject='Welcome to Our School',
                        message='Thankyou for choosing us.',
                        from_email=settings.DEFAULT_FROM_EMAIL,
                        recipient_list=[email],
                        fail_silently=True,
                    )
                except Exception as e:
                    # Email sending failed, but don't interrupt the student creation
                    print(f"Error sending email to {email}: {e}")
            
            messages.success(request, 'Student created successfully!')
            return redirect('student_list')
        except Grade.DoesNotExist:
            messages.error(request, 'Invalid grade selected.')
        except Exception as e:
            messages.error(request, f'Error creating student: {str(e)}')
    
    context = {
        'grades': grades,
        'streams': streams,
    }
    return render(request, 'student/student_form.html', context)

@login_required
@user_passes_test(is_admin)
def student_update(request, pk):
    student = get_object_or_404(Student, pk=pk)
    grades = Grade.objects.all()
    streams = Stream.objects.all()
    
    # Ensure Stream objects exist
    if streams.count() == 0:
        Stream.objects.get_or_create(name='science')
        Stream.objects.get_or_create(name='commerce')
        Stream.objects.get_or_create(name='humanities')
        streams = Stream.objects.all()
    
    if request.method == 'POST':
        student.name = request.POST.get('name')
        student.roll_number = request.POST.get('roll_number')
        grade_id = request.POST.get('grade')
        stream_id = request.POST.get('stream') or None
        student.division = request.POST.get('division')
        student.address = request.POST.get('address')
        student.phone = request.POST.get('phone')
        student.email = request.POST.get('email')
        date_of_birth = request.POST.get('date_of_birth') or None
        student.date_of_birth = date_of_birth
        
        try:
            if grade_id:
                grade = Grade.objects.get(id=grade_id)
                student.grade = grade
            if stream_id:
                try:
                    # Try to get by ID first
                    stream = Stream.objects.get(id=stream_id)
                except (Stream.DoesNotExist, ValueError):
                    # If ID lookup fails, try by name
                    try:
                        stream = Stream.objects.get(name=stream_id)
                    except Stream.DoesNotExist:
                        stream = None
                student.stream = stream
            else:
                student.stream = None
            student.save()
            messages.success(request, 'Student updated successfully!')
            return redirect('student_list')
        except Grade.DoesNotExist:
            messages.error(request, 'Invalid grade selected.')
        except Stream.DoesNotExist:
            messages.error(request, 'Invalid stream selected.')
        except Exception as e:
            messages.error(request, f'Error updating student: {str(e)}')
    
    context = {
        'student': student,
        'grades': grades,
        'streams': streams,
    }
    return render(request, 'student/student_form.html', context)

@login_required
@user_passes_test(is_admin)
def student_delete(request, pk):
    student = get_object_or_404(Student, pk=pk)
    if request.method == 'POST':
        student.delete()
        messages.success(request, 'Student deleted successfully!')
        return redirect('student_list')
    return render(request, 'student/student_confirm_delete.html', {'student': student})

# Student detail view - supports both admin (with pk) and student (own details)
@login_required
def student_detail(request, pk=None):
    # If pk is provided, admin is viewing a specific student
    if pk:
        if not request.user.is_staff:
            messages.error(request, 'You do not have permission to view this page.')
            return redirect('student_list')
        student = get_object_or_404(Student, pk=pk)
        is_admin_view = True
    else:
        # Student viewing their own details (assuming student's roll_number is stored in user.username)
        try:
            student = Student.objects.get(roll_number=request.user.username)
            is_admin_view = False
        except Student.DoesNotExist:
            student = None
            is_admin_view = False
    
    return render(request, 'student/student_detail.html', {
        'student': student,
        'is_admin_view': is_admin_view
    })


# Attendance views
@login_required
@user_passes_test(is_admin)
def attendance_list(request):
    sessions = Attendance.objects.all().order_by('-date')
    return render(request, 'student/attendance_list.html', {'sessions': sessions})


@login_required
@user_passes_test(is_admin)
def attendance_mark(request):
    grades = Grade.objects.all().order_by('grade')
    streams = Stream.objects.all()
    if request.method == 'POST':
        grade_id = request.POST.get('grade')
        stream_id = request.POST.get('stream') or None
        date_str = request.POST.get('date')
        date = date_str and date_str or timezone.localdate()
        grade = Grade.objects.get(pk=grade_id)
        stream = Stream.objects.get(pk=stream_id) if stream_id else None

        # If the POST contains the 'present' checkboxes, this is the save step.
        present_ids = request.POST.getlist('present')
        if present_ids:
            attendance, created = Attendance.objects.get_or_create(date=date, grade=grade, stream=stream)

            # remove any existing records to allow re-submission
            AttendanceRecord.objects.filter(attendance=attendance).delete()

            # students to mark
            if stream:
                students = Student.objects.filter(grade=grade, stream=stream)
            else:
                students = Student.objects.filter(grade=grade)

            records = []
            for s in students:
                present = str(s.pk) in present_ids
                records.append(AttendanceRecord(attendance=attendance, student=s, present=present))
            AttendanceRecord.objects.bulk_create(records)

            # send immediate email per student with today's status
            for rec in attendance.records.select_related('student'):
                student = rec.student
                if not student.email:
                    continue
                subject = f"Attendance for {attendance.date}"
                status = 'Present' if rec.present else 'Absent'
                message = f"Dear {student.name},\n\nYour attendance for {attendance.date} is: {status}.\n\nRegards,\nSchool Admin"
                try:
                    send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [student.email], fail_silently=True)
                except Exception:
                    pass

            messages.success(request, 'Attendance recorded and emails sent where configured.')
            return redirect('attendance_list')

        # Otherwise show the list of students to mark for the selected grade/stream/date
        if stream:
            students = Student.objects.filter(grade=grade, stream=stream).order_by('division', 'name')
        else:
            students = Student.objects.filter(grade=grade).order_by('division', 'name')

        return render(request, 'student/attendance_form.html', {
            'grades': grades,
            'streams': streams,
            'students': students,
            'selected_grade': grade,
            'selected_stream': stream,
            'selected_date': date,
        })

    return render(request, 'student/attendance_form.html', {'grades': grades, 'streams': streams})
