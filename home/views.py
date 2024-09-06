from django.contrib import messages
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.hashers import make_password
from student.forms import *
from django.db.models import Q


# Create your views here.

def home(request):
    tutorials = Tutorial.objects.filter(
        is_published=True
    )
    context = {
        'tutorials': tutorials,
    }
    return render(request, 'home.html', context)

def sign_in(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            user = User.objects.get(id=request.user.id)
            if user.are_you_a_student:
                messages.success(request, "Welcome to Your student's account")
                return redirect('student-dashboard-url')
            else:
                messages.success(request, "Welcome to Your author's account")
                return redirect('author-dashboard-url')
        else:
            messages.error(request, 'Invalid username or password')
            return redirect('home-url')

    return redirect('student-dashboard-url')

def sign_up(request):
    form = UserSignUpForm()
    tutorials = Tutorial.objects.filter(is_published=True)

    if request.method == 'POST':
        form = UserSignUpForm(request.POST)
        password = request.POST.get('password')
        user_type = request.POST.get('user-type')  # '1' for student, '0' for non-student
        reg_number = request.POST.get('reg-number')
        lecturer_username = request.POST.get('lecturer')

        # If the user is a student
        if user_type == '1' and reg_number and lecturer_username:
            try:
                lecturer = User.objects.get(username=lecturer_username)  # Fetch the lecturer
                if form.is_valid():
                    # Save the User first
                    form.instance.password = make_password(password)
                    form.instance.registration_number = reg_number  # Set the registration number for the student
                    form.instance.are_you_a_student = True  # Mark as a student
                    form.save()

                    # Save the StudentApproval instance
                    student_approval = StudentApproval.objects.create(
                        registration_number=reg_number,
                        lecturer=lecturer,  # Assign the selected lecturer
                        is_approved=False  # Default to not approved
                    )
                    student_approval.save()

                    messages.success(request, 'Account created successfully. Awaiting lecturer approval.')
                    return redirect('home-url')
                else:
                    messages.error(request, 'Please correct the errors and try again.')
            except User.DoesNotExist:
                messages.error(request, "Lecturer with that username not found! Ask your lecturer for their username.")
                return redirect('sign-up-url')  # Redirect to the same page to retry the sign-up

        # If the user is NOT a student
        else:
            if form.is_valid():
                form.instance.password = make_password(password)
                form.instance.are_you_a_student = False  # Mark as non-student
                form.instance.registration_number = "NOT STUDENT"  # Registration number is not needed
                form.save()

                messages.success(request, 'Account created successfully.')
                return redirect('home-url')
            else:
                messages.error(request, 'Please correct the errors and try again.')

    context = {
        'tutorials': tutorials,
        'form': form,
    }
    return render(request, 'home.html', context)

def sign_out(request):
    logout(request)
    return redirect('home-url')


def search(request):
    import json
    data = json.loads(request.body)
    query = data.get('query')
    results = Tutorial.objects.filter(
        name__icontains=query,
        is_published=True
    )
    data = list(results.values('id', 'name', 'user__username'))
   
    context = {
        'success': True,
        'data': data
    }
    return JsonResponse(context)
