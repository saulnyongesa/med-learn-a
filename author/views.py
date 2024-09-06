from http.client import responses

from django.contrib import messages
from django.http import JsonResponse, HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from student.forms import *

# Tutorial CRUD operations====
@login_required(login_url='home-url')
def tutorial_view(request, pk):
    user = User.objects.get(id=request.user.id)
    if not user.are_you_a_student:
        current_tutorial = Tutorial.objects.get(id=pk)
        topics = Topic.objects.filter(tutorial=current_tutorial)
        attachments = Attachments.objects.filter(tutorial=current_tutorial)
       
        context = {
            'tutorial': current_tutorial,
            'topics': topics,
            'attachments': attachments,           
        }
        return render(request, 'author/tutorial.html', context)
    else:
        messages.error(request, "Logged in as Student!")
        return redirect('student-dashboard-url')


@login_required(login_url='home-url')
def tutorial_edit(request, pk):
    user = User.objects.get(id=request.user.id)
    if not user.are_you_a_student:
        tutorial = Tutorial.objects.get(id=pk)
        topics = Topic.objects.filter(tutorial=tutorial)
        attachments = Attachments.objects.filter(tutorial=tutorial)
        context = {
            'tutorial': tutorial,
            'topics': topics,
            'attachments': attachments,
        }
        return render(request, 'author/tutorial-edit.html', context)
    else:
        messages.error(request, "Logged in as Student!")
        return redirect('student-dashboard-url')

@login_required(login_url='home-url')
def save_tutorial(request, pk):
    user = User.objects.get(id=request.user.id)
    if not user.are_you_a_student:
        import json
        data = json.loads(request.body)
        tutorial_name = data.get('name')
        tutorial_description = data.get('description')
        tutorial = Tutorial.objects.get(id=pk)
        tutorial.name = tutorial_name
        tutorial.description = tutorial_description
        tutorial.save()
        return JsonResponse({'success': True})
    else:
        messages.error(request, "Logged in as Student!")
        return redirect('student-dashboard-url')


@login_required(login_url='home-url')
def save_topic(request):
    user = User.objects.get(id=request.user.id)
    if not user.are_you_a_student:
        import json
        data = json.loads(request.body)
        topic_id = data.get('id')
        field = data.get('field')
        value = data.get('value')

        try:
            topic = Topic.objects.get(id=topic_id)
            if field == '' or value == '':
                messages.error(request, "Topic name or Notes Can't be blank")
                return HttpResponseRedirect('/Author/Tutorial/Edit/' + str(topic.tutorial.id))
            else:
                setattr(topic, field, value)
                topic.save()
                return JsonResponse({'success': True})
        except Topic.DoesNotExist:
            messages.error(request, 'Topic Was Not Saved, Try Again')
            return JsonResponse({'success': False, 'error': 'Topic not found'})
    else:
        messages.error(request, "Logged in as Student!")
        return redirect('student-dashboard-url')

@login_required(login_url='home-url')
def create_topic(request):
    user = User.objects.get(id=request.user.id)
    if not user.are_you_a_student:
        import json
        data = json.loads(request.body)
        tutorial_id = data.get('id')
        name = data.get('name')
        notes = data.get('notes')
        tutorial = Tutorial.objects.get(id=tutorial_id)
        if name == '' or notes == '':
            messages.error(request, "Topic name or Notes Can't be blank")
            return HttpResponseRedirect('/Author/Tutorial/Edit/' + str(tutorial.id))
        else:
            try:
                Topic.objects.create(
                    tutorial=tutorial,
                    name=name,
                    notes=notes
                )
                messages.success(request, 'Topic saved successfully')
                return JsonResponse({'success': True})
            except Topic.DoesNotExist:
                messages.error(request, 'Topic Was Not Saved, Try Again')
                return JsonResponse({'success': False, 'error': 'Topic failed'})
    else:
        messages.error(request, "Logged in as Student!")
        return redirect('student-dashboard-url')


@login_required(login_url='home-url')
def create_tutorial(request):
    user = User.objects.get(id=request.user.id)
    if not user.are_you_a_student:
        import json
        data = json.loads(request.body)
        name = data.get('name')
        description = data.get('description')
        try:
            Tutorial.objects.create(
                user=request.user,
                name=name,
                description=description
            )
            messages.success(request, 'Tutorial saved successfully')
            return JsonResponse({'success': True})
        except Topic.DoesNotExist:
            messages.error(request, 'Tutorial Was Not Saved, Try Again')
            return JsonResponse({'success': False, 'error': 'Tutorial failed'})
    else:
        messages.error(request, "Logged in as Student!")
        return redirect('student-dashboard-url')

@login_required(login_url='home-url')
def search(request):
    user = User.objects.get(id=request.user.id)
    if not user.are_you_a_student:
        import json
        data = json.loads(request.body)
        query = data.get('query')
        results = Tutorial.objects.filter(
            user = request.user,
            name__icontains=query
        )
        data = list(results.values('id', 'name', 'user__username'))

        context = {
            'success': True,
            'data': data
        }
        return JsonResponse(context)
    else:
        messages.error(request, "Logged in as Student!")
        return redirect('student-dashboard-url')

@login_required(login_url='home-url')
def tutorial_conceal_publish(request, pk):
    user = User.objects.get(id=request.user.id)
    if not user.are_you_a_student:
        try:
            current_tutorial = Tutorial.objects.get(id=pk)
            current_tutorial.is_published = not current_tutorial.is_published
            current_tutorial.save()
            return redirect('author-dashboard-url')
        except Tutorial.DoesNotExist:
            return redirect('author-dashboard-url')
    else:
        messages.error(request, "Logged in as Student!")
        return redirect('student-dashboard-url')

@login_required(login_url='home-url')
def tutorial_delete(request, pk):
    user = User.objects.get(id=request.user.id)
    if not user.are_you_a_student:
        try:
            current_tutorial = Tutorial.objects.get(id=pk)
            current_tutorial.delete()
            messages.error(request, '"' + current_tutorial.name + '" Has Been Deleted Permanently')
            return redirect('author-dashboard-url')
        except Tutorial.DoesNotExist:
            return redirect('author-dashboard-url')
    else:
        messages.error(request, "Logged in as Student!")
        return redirect('student-dashboard-url')

# Account Function====
@login_required(login_url='home-url')
def dashboard_index_author(request):
    user = User.objects.get(id=request.user.id)
    if not user.are_you_a_student:
        my_tutorials = Tutorial.objects.filter(
            user_id=request.user.id
        )
        approvals = StudentApproval.objects.filter(
            lecturer=request.user
        )
        students = User.objects.filter(
            are_you_a_student=True
        )
        context = {
            'my_tutorials': my_tutorials,
            'approvals': approvals,
            'students': students
        }
        return render(request, 'author/index.html', context)
    else:
        messages.error(request, "Logged in as Student!")
        return redirect('student-dashboard-url')

@login_required(login_url='home-url')
def profile(request):
    user = User.objects.get(id=request.user.id)
    if not user.are_you_a_student:
        form = UserDetailsForm(instance=request.user)
        return render(request, 'author/profile.html', {'form': form})
    else:
        messages.error(request, "Logged in as Student!")
        return redirect('author-dashboard-url')


@login_required(login_url='home-url')
def profile_edit(request):
    user = User.objects.get(id=request.user.id)
    if not user.are_you_a_student:
        if request.method == 'POST':
            form = UserEditForm(request.POST, instance=request.user)
            if form.is_valid():
                form.save()
                messages.success(request, 'You edited your profile successfully')
                return redirect('author-profile-url')
            else:
                messages.error(request, 'Please correct the errors')
        else:
            form = UserEditForm(instance=request.user)
        return render(request, 'author/profile-edit.html', {'form': form})
    else:
        messages.error(request, "Logged in as Student!")
        return redirect('student-dashboard-url')



# Exams====
@login_required(login_url='home-url')
def cat_home(request):
    user = User.objects.get(id=request.user.id)
    if not user.are_you_a_student:
        cats = Cat.objects.filter(
            user_id=request.user.id
        )
        context = {
            'cats': cats,
        }
        return render(request, 'cat/cat.html', context)
    else:
        messages.error(request, "Logged in as Student!")
        return redirect('student-dashboard-url')

@login_required(login_url='home-url')
def cat_create(request):
    user = User.objects.get(id=request.user.id)
    if not user.are_you_a_student:
        if request.method == 'POST':
            name = request.POST.get('name')
            start = request.POST.get('start')
            end = request.POST.get('end')
            cat = Cat.objects.create(
                user=request.user,
                name=name,
                start=start,
                end=end
            )
            cat.save()
            messages.success(request, 'Cat/Assignment Created and Saved successfully')
            return redirect('cat-home-url')
    else:
        messages.error(request, "Logged in as Student!")
        return redirect('student-dashboard-url')

@login_required(login_url='home-url')
def cat_view(request, pk):
    user = User.objects.get(id=request.user.id)
    if not user.are_you_a_student:
        try:
            cat = Cat.objects.get(id=pk)
            questions = Question.objects.filter(cat=cat)
            answers = Answer.objects.all()
            user_responses = Response.objects.filter(
                user=request.user,
            )
            context = {
                'cat': cat,
                'questions': questions,
                'answers': answers,
                'responses': user_responses
            }
            return render(request, 'cat/cat_view.html', context)
        except Cat.DoesNotExist:
            messages.error(request, "Cat not available")
            return redirect('cat-home-url')
    else:
        messages.error(request, "Logged in as Student!")
        return redirect('student-dashboard-url')

@login_required(login_url='home-url')
def cat_edit(request):
    user = User.objects.get(id=request.user.id)
    if not user.are_you_a_student:
        return render(request, 'cat/cat_edit.html')
    else:
        messages.error(request, "Logged in as Student!")
        return redirect('student-dashboard-url')

@login_required(login_url='home-url')
def cat_publish_conceal(request, pk):
    user = User.objects.get(id=request.user.id)
    if not user.are_you_a_student:
        try:
            cat = Cat.objects.get(id=pk)
            cat.cat_id = str(request.user.username)+ '/' + str(cat.id)
            cat.is_published = not cat.is_published
            cat.save()
            if cat.is_published:
                messages.success(request, "Cat Published!")
            else:
                messages.success(request, "Cat concealed!")
            return redirect('cat-home-url')
        except Cat.DoesNotExist:
            messages.error(request, "Cat not available")
            return redirect('cat-home-url')
    else:
        messages.error(request, "Logged in as Student!")
        return redirect('student-dashboard-url')


def cat_delete(request, pk):
    user = User.objects.get(id=request.user.id)
    if not user.are_you_a_student:
        try:
            cat = Cat.objects.get(id=pk)
            cat.delete()
            messages.success(request, "Cat deleted!")
            return redirect('cat-home-url')
        except Cat.DoesNotExist:
            messages.error(request, "Cat not available")
            return redirect('cat-home-url')
    else:
        messages.error(request, "Logged in as Student!")
        return redirect('student-dashboard-url')

# Cat Response==============
def cat_response_save(request, pk):
    user = User.objects.get(id=request.user.id)
    if not user.are_you_a_student:
        if request.method == 'POST':
            question = Question.objects.get(id=pk)
            answer_id = request.POST.get('answer-id')
            try:
                response = Response.objects.get(
                    user=request.user,
                    question=question,
                )
                response.answer_id=answer_id
                response.is_correct = True if response.answer.is_correct_answer else False
                response.save()
                return JsonResponse({'success': True})
            except Response.DoesNotExist:
                response = Response.objects.create(
                    user=request.user,
                    question=question,
                    answer_id=answer_id,
                )
                response.is_correct = True if response.answer.is_correct_answer else False
                response.save()
                return JsonResponse({'success': True})
        else:
            return JsonResponse({'success': False}, status=400)
    else:
        return JsonResponse({'success': False, 'message': "Logged in as Student!"}, status=403)

