from django.contrib.auth.models import AbstractUser
from django.db import models


# Create your models here.

class User(AbstractUser):
    phone = models.PositiveIntegerField(null=True, unique=True)
    registration_number = models.CharField(max_length=55, null=True, )
    are_you_a_student = models.BooleanField(default=True)
    updated = models.DateTimeField(auto_now=True, null=True)
    created = models.DateTimeField(auto_now_add=True, null=True)

    class Meta:
        ordering = ['-updated', '-created']

class StudentApproval(models.Model):
    registration_number = models.CharField(max_length=255, null=True, )
    lecturer = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
    is_approved = models.BooleanField(default=False)
    updated = models.DateTimeField(auto_now=True, null=True)
    created = models.DateTimeField(auto_now_add=True, null=True)

    class Meta:
        ordering = ['-updated', '-created']
    
    def __str__(self):
        return self.registration_number


class Tutorial(models.Model):
    user = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=255, null=True, )
    description = models.TextField(max_length=250, null=True, )
    is_published = models.BooleanField(default=False)
    updated = models.DateTimeField(auto_now=True, null=True)
    created = models.DateTimeField(auto_now_add=True, null=True)
    class Meta:
        ordering = ['-updated', '-created']

    def __str__(self):
        return self.name


class Topic(models.Model):
    tutorial = models.ForeignKey(Tutorial, null=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=50, null=True, )
    notes = models.TextField(null=True, )
    updated = models.DateTimeField(auto_now=True, null=True)
    created = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return self.tutorial.name


class Attachments(models.Model):
    tutorial = models.ForeignKey(Tutorial, null=True, on_delete=models.CASCADE)
    file_name = models.CharField(max_length=50, null=True, )
    attachment = models.FileField(upload_to='TutorialAttachments/', null=True, blank=True)
    updated = models.DateTimeField(auto_now=True, null=True)
    created = models.DateTimeField(auto_now_add=True, null=True)

    class Meta:
        ordering = ['-updated', '-created']

    def __str__(self):
        return self.tutorial.name


class MyTutorial(models.Model):
    user = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
    tutorial = models.ForeignKey(Tutorial, null=True, on_delete=models.CASCADE)
    updated = models.DateTimeField(auto_now=True, null=True)
    created = models.DateTimeField(auto_now_add=True, null=True)

    class Meta:
        ordering = ['-updated', '-created']

    def __str__(self):
        return self.tutorial.name


# Cat=====================================
class Cat(models.Model):
    cat_id = models.CharField(max_length=100, null=True, unique=True)
    user = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=255, null=True, )
    start = models.DateTimeField(null=True)
    end = models.DateTimeField(null=True)
    is_published = models.BooleanField(default=False)
    updated = models.DateTimeField(auto_now=True, null=True)
    created = models.DateTimeField(auto_now_add=True, null=True)

    class Meta:
        ordering = ['-updated', '-created']

    def __str__(self):
        return self.name


class Question(models.Model):
    cat = models.ForeignKey(Cat, null=True, on_delete=models.CASCADE)
    question = models.CharField(max_length=50, null=True, )
    updated = models.DateTimeField(auto_now=True, null=True)
    created = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return self.question + ' -- ' +self.cat.name


class Answer(models.Model):
    question = models.ForeignKey(Question, null=True, on_delete=models.CASCADE)
    answer = models.CharField(max_length=50, null=True, )
    is_correct_answer = models.BooleanField(default=False)
    updated = models.DateTimeField(auto_now=True, null=True)
    created = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return '"' + self.answer + '"' + ' For ' + self.question.question + ' -CAT: ' + self.question.cat.name


class Response(models.Model):
    user = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, null=True, on_delete=models.CASCADE)
    answer = models.ForeignKey(Answer, null=True, on_delete=models.CASCADE)
    is_selected = models.BooleanField(default=True)
    updated = models.DateTimeField(auto_now=True, null=True)
    created = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return self.answer.answer + '--' + self.question.question + '---' + self.question.cat.name

class CatSubmit(models.Model):
    user = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
    cat = models.ForeignKey(Cat, null=True, on_delete=models.CASCADE)
    is_submitted = models.BooleanField(default=True)
    updated = models.DateTimeField(auto_now=True, null=True)
    created = models.DateTimeField(auto_now_add=True, null=True)

    class Meta:
        ordering = ['-updated', '-created']

    def __str__(self):
        return self.cat.name
