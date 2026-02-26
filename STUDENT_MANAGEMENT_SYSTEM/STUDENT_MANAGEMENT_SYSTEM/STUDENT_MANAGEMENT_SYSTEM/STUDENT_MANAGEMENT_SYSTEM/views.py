from django.shortcuts import render,redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from student.models import registrationstudent

def index1(request):
    
    return render(request,"index.html")

@login_required
def admindash(request):
    return render(request,"admindashboard.html")

def login_view(request):
    if request.method == 'POST':
        # username=request.POST.get('username')
        # password=request.POST.get('password')
        # if username=="hiren@gmail.com" and password=="1234":
        #     return redirect('admin')
        # else:
        #     return redirect('login')
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            if user.is_superuser:
                return render(request,"admindashboard.html")
            else:
                return render(request,"student_welcome.html")
    else:
        form = AuthenticationForm()
    return render(request, 'login.html')


def register(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        phone=request.POST.get('phone')
        dob=request.POST.get('dob')
        gender=request.POST.get('gender')
        course=request.POST.get('course')
        address=request.POST.get('address')
        password = request.POST.get('password')
        confirmpassword = request.POST.get('confirmpassword')
        user=registrationstudent(first_name=first_name,last_name=last_name,email=email,phone=phone,dob=dob,
                                 gender=gender,course=course,address=address,password=password,confirmpassword=confirmpassword)
        user.save()
        # Use email as username
        username = email

        if len(password) < 6 or len(confirmpassword) < 6:
            return render(request, 'register.html', {'error': 'Password must be at least 6 characters.'})
        if password != confirmpassword:
            return render(request, 'register.html', {'error': 'Passwords do not match.'})
        if User.objects.filter(username=username).exists():
            return render(request, 'register.html', {'error': 'Email already registered as username.'})
        if User.objects.filter(email=email).exists():
            return render(request, 'register.html', {'error': 'Email already exists.'})
        user = User.objects.create_user(username=username, email=email, password=password, first_name=first_name, last_name=last_name)
        user.save()
       # Authenticate and login
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('login')  # Redirect to login page
    return render(request, 'register.html')

