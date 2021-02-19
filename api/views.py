from django.shortcuts import render

# Create your views here.
import datetime
from rest_framework import viewsets, decorators, response

from django_filters.rest_framework import DjangoFilterBackend

from .serializers import QuizSerializer, QuestionSerializer, SummarySerializer

from .models import Quiz, Question, Summary


class QuizViewSet(viewsets.ModelViewSet):
    queryset = Quiz.objects.all()
    serializer_class = QuizSerializer
    #permission_classes = (PollPermission\)


class QuestionViewSet(viewsets.ModelViewSet):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer


class SummaryViewSet(viewsets.ModelViewSet):
    queryset = Summary.objects.all()
    serializer_class = SummarySerializer
