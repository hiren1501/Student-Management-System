from django.shortcuts import render,redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from student.models import registrationstudent
from student.student_crud_models import Student, Grade
from course.models import courses
from faculty.models import faculties

def index1(request):
    
    return render(request,"index.html")

@login_required
def admindash(request):

    # compute totals for dashboard
    # Count admin-managed Student records (used by admin CRUD views)
    total_students = Student.objects.count()
    total_courses = courses.objects.count()
    total_faculties = faculties.objects.count()
    context = {
        'total_students': total_students,
        'total_courses': total_courses,
        'total_faculties': total_faculties,
    }


    return render(request, "admindashboard.html", context)


def login_view(request):
    if request.method == 'POST':
        username_or_email = request.POST.get('username', '').strip()
        password = request.POST.get('password', '')
        
        # Try to find user by email if @ is in the input
        user = None
        if '@' in username_or_email:
            # User entered email, try to authenticate with email
            try:
                user_obj = User.objects.get(email=username_or_email)
                username = user_obj.username
                user = authenticate(request, username=username, password=password)
            except User.DoesNotExist:
                user = None
        else:
            # User entered username, authenticate normally
            user = authenticate(request, username=username_or_email, password=password)
        
        if user is not None:
            login(request, user)
            if user.is_superuser:
                # redirect to admindash which will populate counts
                return redirect('admin')
            elif user.is_staff:
                # Faculty login
                try:
                    faculty = faculties.objects.get(email=user.email)
                except faculties.DoesNotExist:
                    faculty = None
                return render(request, "faculty_welcome.html", {'faculty': faculty})
            else:
                # Student login - redirect to student welcome page
                return redirect('student_welcome_page')
        else:
            # Authentication failed
            messages.error(request, 'Invalid email/username or password.')
            return render(request, 'login.html', {'error': 'Invalid email/username or password.'})
    
    return render(request, 'login.html')


@login_required
def faculty_welcome(request):
    try:
        faculty = faculties.objects.get(email=request.user.email)
    except faculties.DoesNotExist:
        faculty = None
    return render(request, "faculty_welcome.html", {'faculty': faculty})


def register(request):
    if request.method == 'POST':
        user_type = request.POST.get('user_type', 'student')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        address = request.POST.get('address')
        password = request.POST.get('password')
        confirmpassword = request.POST.get('confirmpassword')
        
        # Validate passwords
        if len(password) < 6 or len(confirmpassword) < 6:
            return render(request, 'register.html', {'error': 'Password must be at least 6 characters.'})
        if password != confirmpassword:
            return render(request, 'register.html', {'error': 'Passwords do not match.'})
        
        # Use email as username
        username = email
        
        if User.objects.filter(username=username).exists():
            return render(request, 'register.html', {'error': 'Email already registered as username.'})
        if User.objects.filter(email=email).exists():
            return render(request, 'register.html', {'error': 'Email already exists.'})
        
        if user_type == 'faculty':
            # Faculty registration
            qualification = request.POST.get('qualification', '')
            experience_years = request.POST.get('experience_years', 0)
            
            try:
                experience_years = int(experience_years)
            except:
                experience_years = 0
            
            # Generate faculty ID
            import random
            import string
            faculty_id = 'FAC' + ''.join(random.choices(string.digits, k=7))
            
            # Check if faculty ID already exists
            while faculties.objects.filter(id=faculty_id).exists():
                faculty_id = 'FAC' + ''.join(random.choices(string.digits, k=7))
            
            # Save faculty record
            faculty = faculties(
                id=faculty_id,
                name=f"{first_name} {last_name}",
                email=email,
                phone=phone,
                address=address,
                qualification=qualification,
                experience_years=experience_years
            )
            faculty.save()
            
            # Create Django user with is_staff=True for faculty
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password,
                first_name=first_name,
                last_name=last_name,
                is_staff=True
            )
            user.save()
            
            # Send welcome email
            try:
                send_mail(
                    subject='Welcome to Our School - Faculty Portal',
                    message=f'Welcome {first_name}! Your faculty ID is: {faculty_id}',
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[email],
                    fail_silently=False,
                )
            except Exception as e:
                print(f"Error sending email: {e}")
            
            # Authenticate and login
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('faculty_welcome')  # You can create this view later
        
        else:
            # Student registration (existing code)
            dob = request.POST.get('dob')
            gender = request.POST.get('gender')
            course = request.POST.get('course', '')
            
            # Save registration student record
            student = registrationstudent(
                first_name=first_name,
                last_name=last_name,
                email=email,
                phone=phone,
                dob=dob,
                gender=gender,
                course=course,
                address=address,
                password=password,
                confirmpassword=confirmpassword
            )
            student.save()
            
            # Create Django user
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password,
                first_name=first_name,
                last_name=last_name
            )
            user.save()
            
            # Create Student record for admin management
            try:
                full_name = f"{first_name} {last_name}".strip()
                
                import random
                import string
                roll_number_base = email.split('@')[0][:10].upper()
                roll_number = roll_number_base
                counter = 1
                
                while Student.objects.filter(roll_number=roll_number).exists():
                    roll_number = f"{roll_number_base}{counter}"
                    counter += 1
                
                default_grade, _ = Grade.objects.get_or_create(grade=1)
                
                student_record = Student.objects.create(
                    name=full_name,
                    roll_number=roll_number,
                    grade=default_grade,
                    stream=None,
                    division='A',
                    address=address,
                    phone=phone if phone else '',
                    email=email,
                    date_of_birth=dob if dob else None
                )
            except Exception as e:
                print(f"Error creating Student record: {e}")
            
            # Send welcome email
            try:
                send_mail(
                    subject='Welcome to Our School',
                    message='Thank you for choosing our school',
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[email],
                    fail_silently=False,
                )
            except Exception as e:
                print(f"Error sending email: {e}")
            
            # Authenticate and login
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('login')
    
    return render(request, 'register.html')


@login_required
@user_passes_test(lambda u: u.is_staff)
def course_add(request):
    if request.method=="POST":
        subject_id=request.POST.get('subject_id')
        subject_name=request.POST.get('subject_name')
        faculty_name=request.POST.get('faculty_name')
        try:
            courses.objects.create(subject_id=subject_id,subject_name=subject_name,faculty_name=faculty_name)
            messages.success(request, 'Course created successfully!')
            return redirect('course_view')
        except Exception as e:
            messages.error(request, f'Error creating course: {str(e)}')
    return render(request,"course_add.html")

@login_required
@user_passes_test(lambda u: u.is_staff)
def course_view(request):
    course=courses.objects.all()
    data={'course':course}
    return render(request,"course_view.html",data)

def timetable_view(request):
    return render(request, "timetable.html")

@login_required
@user_passes_test(lambda u: u.is_staff)
def course_update(request,subject_id):
    try:
        course = courses.objects.get(subject_id=subject_id)
    except courses.DoesNotExist:
        messages.error(request, 'Course not found.')
        return redirect('course_view')
    
    if request.method == "POST":
        # Don't update the subject_id (primary key) - it's read-only
        course.subject_name = request.POST.get('subject_name')
        course.faculty_name = request.POST.get('faculty_name')
        try:
            course.save()
            messages.success(request, 'Course updated successfully!')
            return redirect('course_view')
        except Exception as e:
            messages.error(request, f'Error updating course: {str(e)}')
    return render(request,"course_update.html",{'course':course})

@login_required
@user_passes_test(lambda u: u.is_staff)
def course_delete(request,subject_id):
    try:
        course = courses.objects.get(subject_id=subject_id)
    except courses.DoesNotExist:
        messages.error(request, 'Course not found.')
        return redirect('course_view')
    
    if request.method == "POST":
        try:
            course.delete()
            messages.success(request, 'Course deleted successfully!')
            return redirect('course_view')
        except Exception as e:
            messages.error(request, f'Error deleting course: {str(e)}')
    return render(request,"course_delete.html",{'course':course})





