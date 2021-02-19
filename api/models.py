

# Create your models here.
import datetime
from django.contrib.auth import get_user_model
from django.db import models


class Question(models.Model):
    MY_CHOICES = (
        ('TEXT', 'TEXT'),
        ('CHOICE', 'CHOICE'),
        ('MULTICHOICE', 'MULTICHOICE'),
    )
    quiz = models.ForeignKey('Quiz', on_delete=models.CASCADE)
    text = models.CharField(max_length=256)
    choice = models.CharField(
        max_length=11, choices=MY_CHOICES)


class Choice(models.Model):
    question = models.ForeignKey(
        'Question', related_name='choices', on_delete=models.CASCADE
    )
    text = models.CharField(max_length=10, default='Pick one')


class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice = models.ForeignKey(Choice, on_delete=models.CASCADE)
    value = models.CharField(max_length=128, blank=True, null=True)


class Quiz(models.Model):
    title = models.CharField(max_length=256)
    description = models.TextField(max_length=1024)
    start_date = models.DateField()
    end_date = models.DateField()


class Summary(models.Model):
    Quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    user = models.ForeignKey(
        get_user_model(), on_delete=models.CASCADE, blank=True, null=True)
    date = models.DateField(default=datetime.date.today(), editable=False)
