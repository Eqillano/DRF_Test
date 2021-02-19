import datetime
from django.contrib.auth import get_user_model
from rest_framework import serializers

from .models import Quiz, Question, Choice, Answer, Summary

from django.core.exceptions import ObjectDoesNotExist


class ObjectIDField(serializers.PrimaryKeyRelatedField):

    def to_internal_value(self, data):
        try:
            value = self.get_queryset().get(pk=data)
            return value.id
        except ObjectDoesNotExist:
            self.fail('does_not_exist', pk_value=data)
        except (TypeError, ValueError):
            self.fail('incorrect_type', data_type=type(data).__name__)


class ChoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Choice
        fields = ('text',)


class QuestionSerializer(serializers.ModelSerializer):
    choices = serializers.ChoiceField(
        choices=Question.MY_CHOICES
    )
    choice = ChoiceSerializer(many=True, required=False)

    class Meta:
        model = Question
        fields = ('quiz', 'text', 'choices', 'choice')
        extra_kwargs = {
            'quiz': {'write_only': True}
        }

    def create_choices(self, question, choices):
        Choice.objects.bulk_create([
            Choice(question=question, **d) for d in choices
        ])

    def create(self, validated_data):
        choices = validated_data.pop('choices', [])
        question = Question.objects.create(**validated_data)
        self.create_choices(question, choices)
        return question

    def update(self, instance, validated_data):
        choices = validated_data.pop('choices', [])
        instance.choices.all().delete()
        self.create_choices(instance, choices)
        for key, value in validated_data.items():
            setattr(instance, key, value)
        instance.save()
        return instance


class QuizSerializer(serializers.ModelSerializer):
    questions = QuestionSerializer(many=True, read_only=True)

    class Meta:
        model = Quiz
        fields = ('title', 'start_date',
                  'end_date', 'description', 'questions')

    def validate_start_date(self, value):
        if self.instance and self.instance.start_date < value:
            raise serializers.ValidationError(
                "Changing the date is not allowed!"
            )

        return value


class AnswerSerializer(serializers.ModelSerializer):
    question = QuestionSerializer(read_only=True)
    question_id = ObjectIDField(
        queryset=Question.objects.all(), write_only=True)
    choice = ChoiceSerializer(read_only=True)
    choice_id = ObjectIDField(queryset=Choice.objects.all(), write_only=True)

    class Meta:
        model = Answer
        fields = ('id', 'question_id', 'question',
                  'choice_id', 'choice', 'value')
        read_only_fields = ('id',)


class SummarySerializer(serializers.ModelSerializer):
    answers = AnswerSerializer(many=True)
    quiz = QuizSerializer(read_only=True)
    quiz_id = ObjectIDField(
        queryset=Quiz.objects.filter(end_date__gte=datetime.date.today()),
        write_only=True
    )

    class Meta:
        model = Summary
        fields = ('id', 'quiz_id', 'quiz', 'user', 'date', 'answers')
        read_only_fields = ('id', 'user', 'date')

    def create(self, validated_data):
        answers = validated_data.pop('answers', [])
        instance = Summary.objects.create(**validated_data)
        Answer.objects.bulk_create([
            Answer(summary=instance, **a) for a in answers
        ])
        return instance
