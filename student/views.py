import datetime
from django.utils import timezone
from django.contrib import messages
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.utils.functional import empty

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

# Cat And Assignment=========================
# Exams====
def cat_search(request):
    import json
    data = json.loads(request.body)
    query = data.get('query')
    end_time_check = timezone.now()
    try:
        result = Cat.objects.get(
            cat_id=query,
            is_published=True,
        )
        try:
            CatSubmit.objects.get(
                cat_id=result.id,
                user=request.user,
            )
            context = {
                'success': False,
            }
            return JsonResponse(context)

        except CatSubmit.DoesNotExist:
            data = {
                'id': result.id,
                'name': result.name,
                'username': result.user.username,
                'start': result.start,
                'end': result.end
            }
            context = {
                'success': True,
                'data': data
            }
            return JsonResponse(context)

    except Cat.DoesNotExist:
        context = {
            'success': False,
        }
        return JsonResponse(context)


@login_required(login_url='home-url')
def cat_home(request):
    user = User.objects.get(id=request.user.id)
    if user.are_you_a_student:
        cats = CatSubmit.objects.filter(user_id=request.user.id)
        answers = Response.objects.filter(user=request.user, answer__is_correct_answer=True)
        questions = Question.objects.all()

        for cat in cats:
            cat_questions = questions.filter(cat=cat.cat)
            cat.correct_answers_count = answers.filter(question__in=cat_questions).count()
            cat.total_questions_count = cat_questions.count()

        end_time_check = timezone.now()
        context = {
            'cats': cats,
            'end_time_check': end_time_check,
        }
        return render(request, 'student/cat.html', context)
    else:
        messages.error(request, "Logged in as author!")
        return redirect('author-dashboard-url')


@login_required(login_url='home-url')
def cat_view(request, pk):
    user = User.objects.get(id=request.user.id)
    if user.are_you_a_student:
        try:
            cat = Cat.objects.get(id=pk)
            questions = Question.objects.filter(cat=cat)
            answers = Answer.objects.all()
            user_responses = Response.objects.filter(
                user=request.user,
            )
            try:
                CatSubmit.objects.get(
                    user=request.user,
                    cat=cat,
                )
            except CatSubmit.DoesNotExist:
                cat_submit = CatSubmit.objects.create(
                    user=request.user,
                    cat=cat,
                    is_submitted=False
                )
                cat_submit.save()
            end_time_check = cat.end < timezone.now()
            context = {
                'cat': cat,
                'questions': questions,
                'answers': answers,
                'responses': user_responses,
                'end_time_check': end_time_check,
            }
            return render(request, 'student/cat_view.html', context)
        except Cat.DoesNotExist:
            messages.error(request, "Cat not available")
            return redirect('cat-home-url')
    else:
        messages.error(request, "Logged in as Author!")
        return redirect('author-dashboard-url')

def cat_response_save(request, pk):
    user = User.objects.get(id=request.user.id)
    if user.are_you_a_student:
        if request.method == 'POST':
            answer_id = request.POST.get('answer-id')
            try:
                question = Question.objects.get(id=pk)
                try:
                    answer = Answer.objects.get(
                        id=answer_id
                    )
                    try:
                        response = Response.objects.get(
                            user=request.user,
                            question=question,
                        )
                        response.answer = answer
                        response.save()
                        return JsonResponse({'success': True})
                    except Response.DoesNotExist:
                        response = Response.objects.create(
                            user=request.user,
                            question=question,
                            answer=answer,
                            is_selected=True
                        )
                        response.save()
                        return JsonResponse({'success': True})
                except Answer.DoesNotExist:
                    return JsonResponse({'success': False})
            except Question.DoesNotExist:
                return JsonResponse({'success': False})
    else:
        return JsonResponse({'success': False, 'message': "Logged in as Student!"}, status=403)

def cat_submission(request, pk):
    user = User.objects.get(id=request.user.id)
    if user.are_you_a_student:
        try:
            cat = Cat.objects.get(id=pk)
            try:
                CatSubmit.objects.get(
                    user=request.user,
                    cat_id=cat.id
                )
                messages.success(request, 'Cat was submitted successfully!')
                return redirect('student-cat-home-url')
            except CatSubmit.DoesNotExist:
                cat_submit = CatSubmit.objects.create(
                    user=request.user,
                    cat=cat,
                    is_submitted=True
                )
                cat_submit.save()
                messages.success(request, 'Cat submitted successfully!')
                return redirect('student-cat-home-url')

        except Cat.DoesNotExist:
            messages.error(request, 'An error occurred during submission! Resubmit The cat again.')
            return redirect('student-cat-home-url')
    else:
        messages.error(request, "Logged in as Author!")
        return redirect('author-dashboard-url')
