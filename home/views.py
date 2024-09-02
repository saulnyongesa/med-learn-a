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
    tutorials = Tutorial.objects.filter(
        is_published=True
    )
    if request.method == 'POST':
        form = UserSignUpForm(request.POST)
        password = request.POST.get('password')
        if form.is_valid():
            form.instance.password = make_password(password)
            form.save()
            messages.success(request, 'Account Created successfully')
            return redirect('home-url')
        else:  
            messages.error(request, 'Please correct the errors and try again')
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
