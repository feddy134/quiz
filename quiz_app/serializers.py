from rest_framework import serializers
from .models import Category, Question, MCQOptions, FillInTheBlank, Progress, StudentQuestion
from users.models import User


class UserSerializer(serializers.ModelSerializer):
    """
    Serializes an `users.User` instance
    """
    class Meta:
        model = User
        fields = ['id', 'user_display_name']


class CategorySerializer(serializers.ModelSerializer):
    """
    Serializes an `Category` instance. 
    related to : `users.User`
    """
    author = UserSerializer(read_only=True)
    image = serializers.ImageField(
        max_length=None, use_url=True
    )

    class Meta:
        model = Category
        fields = ['id', 'author', 'image',
                  'title', 'time_limit', 'description']


class QuestionSerializer(serializers.ModelSerializer):

    category = CategorySerializer(read_only=True)

    class Meta:
        model = Question
        fields = '__all__'


class MCQOptionsSerializer(serializers.ModelSerializer):

    question = QuestionSerializer(read_only=True)

    class Meta:
        model = MCQOptions
        fields = '__all__'


class FillInTheBlankSerializer(serializers.ModelSerializer):

    question = QuestionSerializer(read_only=True)

    class Meta:
        model = FillInTheBlank
        fields = '__all__'


class ProgressSerializaer(serializers.ModelSerializer):
    student = UserSerializer(read_only=True)
    category = CategorySerializer(read_only=True)

    class Meta:
        model = Progress
        fields = '__all__'


class StudentQuestionSerializer(serializers.ModelSerializer):
    question = QuestionSerializer(read_only=True)
    option_choosed = MCQOptionsSerializer(read_only=True)

    class Meta:
        model = StudentQuestion
        fields = '__all__'
