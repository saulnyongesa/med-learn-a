from django.contrib import messages
from django.shortcuts import redirect, render
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from student.forms import *


# from django.db.models import Q

# Create your views here.
@login_required(login_url='home-url')
def dashboard_index_student(request):
    user = User.objects.get(id=request.user.id)
    if user.are_you_a_student:
        latest_tutorials = Tutorial.objects.filter(
            is_published=True
        )
        my_tutorials = MyTutorial.objects.filter(
            user__are_you_a_student=True,
            user_id=request.user.id,
            tutorial__is_published=True
        )
        context = {
            'tutorials': latest_tutorials,
            'my_tutorials': my_tutorials,
        }
        return render(request, 'student/index.html', context)
    else:
        messages.error(request, "Logged in as author!")
        return redirect('author-dashboard-url')

@login_required(login_url='home-url')
def tutorial(request, pk):
    user = User.objects.get(id=request.user.id)
    if user.are_you_a_student:
        try:
            current_tutorial = Tutorial.objects.get(id=pk)
            if current_tutorial.is_published:
                try:
                    MyTutorial.objects.get(
                        user=request.user,
                        tutorial=current_tutorial
                    )
                except MyTutorial.DoesNotExist:
                    MyTutorial.objects.create(
                        user=request.user,
                        tutorial=current_tutorial
                    )
                    messages.success(request, 'Welcome! This tutorial has been Added to your "My tutorials" list.')
                topics = Topic.objects.filter(tutorial=current_tutorial)
                attachments = Attachments.objects.filter(tutorial=current_tutorial)
                context = {
                    'tutorial': current_tutorial,
                    'topics': topics,
                    'attachments': attachments,
                }
                return render(request, 'student/tutorial.html', context)
            else:
                messages.error(request, 'The tutorial is unavailable at the moment.')
                return redirect('student-dashboard-url')
        except Tutorial.DoesNotExist:
            return redirect('student-dashboard-url')
    else:
        messages.error(request, "Logged in as author!")
        return redirect('author-dashboard-url')


@login_required(login_url='home-url')
def tutorial_remove_from_recently_viewed(request, pk):
    user = User.objects.get(id=request.user.id)
    if user.are_you_a_student:
        try:
            current_tutorial = Tutorial.objects.get(id=pk)
            try:
                my_tutorial = MyTutorial.objects.get(
                    user=request.user,
                    tutorial=current_tutorial
                )
                my_tutorial.delete()
            except MyTutorial.DoesNotExist:
                return redirect('student-dashboard-url')
        except Tutorial.DoesNotExist:
            return redirect('student-dashboard-url')
        return redirect('student-dashboard-url')
    else:
        messages.error(request, "Logged in as author!")
        return redirect('author-dashboard-url')

# Account Control Functions==
def sign_out(request):
    logout(request)
    return redirect('home-url')


@login_required(login_url='student-sign-in-url')
def profile(request):
    user = User.objects.get(id=request.user.id)
    if user.are_you_a_student:
        form = UserDetailsForm(instance=request.user)
        return render(request, 'student/profile.html', {'form': form})

    else:
        messages.error(request, "Logged in as author!")
        return redirect('author-dashboard-url')

@login_required(login_url='student-sign-in-url')
def profile_edit(request):
    user = User.objects.get(id=request.user.id)
    if user.are_you_a_student:
        if request.method == 'POST':
            form = UserEditForm(request.POST, instance=request.user)
            if form.is_valid():
                form.save()
                messages.success(request, 'You edited your profile successfully')
                return redirect('student-profile-url')
            else:
                messages.error(request, 'Please correct the errors')
        else:
            form = UserEditForm(instance=request.user)
        return render(request, 'student/profile-edit.html', {'form': form})
    else:
        messages.error(request, "Logged in as author!")
        return redirect('author-dashboard-url')