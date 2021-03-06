from django.shortcuts import render, get_object_or_404
from rest_framework.generics import ListAPIView, CreateAPIView, RetrieveAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from .permissions import TeacherPermission, StudentPermission
from .models import Category, Question, MCQOptions, FillInTheBlank, Progress, StudentQuestion
from .serializers import (CategorySerializer, QuestionSerializer, UserSerializer,
                          MCQOptionsSerializer, FillInTheBlankSerializer, ProgressSerializaer, StudentQuestionSerializer
                          )
from django.utils import timezone
from django.db import transaction
# Create your views here.


class CategoryListView(ListAPIView):
    permission_classes = [IsAuthenticated, StudentPermission]
    # queryset = Category.objects.filter().order_by('title')
    serializer_class = CategorySerializer

    def get_queryset(self, *args, **kwargs):
        final_categories = []
        categories = Category.objects.order_by('title')

        for category in categories:
            progress = Progress.objects.filter(
                student=self.request.user, category=category).first()
            if progress is None:
                final_categories.append(category)
        return final_categories


class CreateCategoryView(CreateAPIView):
    permission_classes = [IsAuthenticated, TeacherPermission]

    def create(self, request, *args, **kwargs):
        request_data = request.data
        serializer = CategorySerializer(data=request_data)
        data = {}
        if serializer.is_valid():
            validated_data = serializer.validated_data
            Category.objects.create(author=request.user, **validated_data)
            data['success'] = 'Category created successfully'
        else:

            data = serializer.errors
        return Response(data)


class QuestionListView(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = QuestionSerializer

    def get_queryset(self, *args, **kwargs):
        return Question.objects.filter(category__id=self.kwargs['category_pk'])


class QuestionDetailsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(sef, request, question_pk):
        data = {}
        question = get_object_or_404(Question, id=question_pk)
        if question.type_of_question == Question.MCQ:
            mcq_options = MCQOptions.objects.filter(question=question)
            serialized_mcqs = []
            for mcq in mcq_options:
                serializer = MCQOptionsSerializer(mcq)
                serialized_mcqs.append(serializer.data)

            data = serialized_mcqs
        if question.type_of_question == Question.FILL_IN_THE_BLANKS:
            fill_in_the_blank = get_object_or_404(
                FillInTheBlank, question=question)
            serializer = FillInTheBlankSerializer(fill_in_the_blank)
            data = serializer.data

        return Response(data=data)


class CreateQuestionView(CreateAPIView):
    permission_classes = [IsAuthenticated, TeacherPermission]

    def create(self, request, *args, **kwargs):
        request_data = request.data
        category = get_object_or_404(Category, id=kwargs['category_pk'])

        question_serializer = QuestionSerializer(data=request_data)
        data = {}

        if question_serializer.is_valid():
            validated_data = question_serializer.validated_data
            if validated_data['type_of_question'] == Question.MCQ:
                options_list = []
                for key, value in request_data.items():
                    if 'option' in key:
                        options_list.append(value)

                if len(options_list) == 0:
                    data['option'] = ["Atleast one option is required."]
                else:
                    all_serializers_valid = True
                    any_one_option_true = False
                    true_count = 0
                    for option in options_list:
                        mcq_serializer = MCQOptionsSerializer(data=option)
                        if mcq_serializer.is_valid():
                            if mcq_serializer.validated_data['is_correct']:
                                any_one_option_true = True
                                true_count += 1
                        else:
                            all_serializers_valid = False
                            data = mcq_serializer.errors

                    if not any_one_option_true:
                        data['error'] = ['Atleast one option must be true']
                        return Response(data)
                    if true_count > 1:
                        data['error'] = ['There should be only one true option']
                        return Response(data)

                    # creating instances
                    if all_serializers_valid and any_one_option_true:
                        question = Question.objects.create(
                            category=category, **question_serializer.validated_data)
                        for option in options_list:
                            mcq_serializer = MCQOptionsSerializer(data=option)
                            if mcq_serializer.is_valid():
                                MCQOptions.objects.create(
                                    question=question, **mcq_serializer.validated_data)

                        data['success'] = "Question added successfully"

            if validated_data['type_of_question'] == Question.FILL_IN_THE_BLANKS:
                fill_the_blank_serializer = FillInTheBlankSerializer(
                    data=request_data)
                if fill_the_blank_serializer.is_valid():
                    question = Question.objects.create(
                        category=category, **question_serializer.validated_data)
                    FillInTheBlank.objects.create(
                        question=question, **fill_the_blank_serializer.validated_data)

                    data['success'] = "Question added successfully"
                else:
                    data = fill_the_blank_serializer.errors

        else:
            data = question_serializer.errors

        return Response(data)


class ProgressByCategoryListView(ListAPIView):
    permission_classes = [IsAuthenticated, TeacherPermission]
    serializer_class = ProgressSerializaer

    def get_queryset(self, *args, **kwargs):
        return Progress.objects.filter(category__id=self.kwargs['category_pk'])


class CategoriesByAuthorView(ListAPIView):
    permission_classes = [IsAuthenticated, TeacherPermission]
    serializer_class = CategorySerializer

    def get_queryset(self, *args, **kwargs):
        return Category.objects.filter(author=self.request.user)


class AttendQuizView(APIView):
    permission_classes = [IsAuthenticated, StudentPermission]

    def get(self, request, category_pk):
        category = get_object_or_404(Category, id=category_pk)
        student_progress = Progress.objects.filter(
            category=category, student=request.user).first()

        # check if questions are present
        questions_count = Question.objects.filter(category=category).count()
        if questions_count == 0:
            return Response({'data': 'No questions available'})
        data = {'category_id': category_pk}

        if student_progress is None:
            now = timezone.now()
            student_progress = Progress.objects.create(category=category,
                                                       start_time=now,
                                                       end_time=now +
                                                       timezone.timedelta(
                                                           minutes=category.time_limit),
                                                       is_in_progress=True,
                                                       student=request.user)

        if student_progress:
            diff = student_progress.end_time-timezone.now()
            if diff < timezone.timedelta(seconds=1):
                data['remaining_seconds'] = 0
            else:
                data['remaining_seconds'] = diff.seconds

        student_questions = StudentQuestion.objects.filter(
            student=request.user, question__category=category, is_attempted=True).values_list('question')

        all_student_questions = Question.objects.filter(category=category)

        if student_questions.count() == all_student_questions.count():
            if all_student_questions.count() > 0:
                student_progress.is_in_progress = False
                student_progress.is_completed = True
                student_progress.save()

        question = Question.objects.filter(
            category=category).exclude(id__in=student_questions).first()

        if question is None:
            if student_progress:
                if student_progress.is_completed:
                    data['data'] = 'completed'

        else:
            data['question'] = QuestionSerializer(instance=question).data
            if question.type_of_question == Question.MCQ:
                options = MCQOptions.objects.filter(question=question)
                for index, option in enumerate(options):
                    data['option_' +
                         str(index)] = MCQOptionsSerializer(instance=option).data

        return Response(data=data)

    def post(self, request, category_pk):
        request_data = request.data

        question_id = request_data['question_id']
        question = get_object_or_404(Question, id=question_id)

        student_progress = Progress.objects.filter(
            category=question.category, student=request.user).first()

        if question.type_of_question == Question.MCQ:
            selected_option_id = request_data.get('selected_option_id', None)
            if(selected_option_id):
                pass
            else:
                return Response(data={'error': ['Select an option']})
            mcq_option = get_object_or_404(MCQOptions, id=selected_option_id)

            student_questions = StudentQuestion.objects.create(
                student=request.user, question=question,
                option_choosed=mcq_option, is_correct=mcq_option.is_correct,
                is_attempted=True)

            if mcq_option.is_correct:
                student_progress.marks = student_progress.marks + 1
                student_progress.save()
        else:
            answer_given = request_data.get('answer_given', None)
            if(answer_given):
                pass
            else:
                return Response(data={'error': ['Answer Required']})
            fill_in_the_blank = get_object_or_404(
                FillInTheBlank, question=question)
            is_correct = False
            if answer_given.lower() == fill_in_the_blank.correct_answer.lower():
                is_correct = True
                student_progress.marks = student_progress.marks + 1
                student_progress.save()

            student_questions = StudentQuestion.objects.create(
                student=request.user, question=question,
                answer_given=answer_given, is_correct=is_correct,
                is_attempted=True)

        return Response({'data': 'Response recorded'})


class ResultView(APIView):
    permission_classes = [IsAuthenticated, StudentPermission]

    def get(self, request, category_pk):
        data = {}
        try:
            progress = Progress.objects.get(
                category__id=category_pk, student=request.user)
            serializer = ProgressSerializaer(instance=progress)
            data = serializer.data

            data['questions_count'] = Question.objects.filter(
                category__id=category_pk).count()

            student_questions = StudentQuestion.objects.filter(
                student=request.user, question__category__id=category_pk)
            data['student_questions'] = []
            for student_question in student_questions:
                student_question_serializer_data = StudentQuestionSerializer(
                    instance=student_question).data
                if student_question.question.type_of_question == Question.MCQ:
                    mcq_option = MCQOptions.objects.filter(
                        question=student_question.question, is_correct=True).first()
                    if mcq_option is not None:
                        student_question_serializer_data['display_correct_answer'] = mcq_option.option
                else:
                    fill_in_the_blank = FillInTheBlank.objects.get(
                        question=student_question.question)
                    student_question_serializer_data['display_correct_answer'] = fill_in_the_blank.correct_answer

                data['student_questions'].append(
                    student_question_serializer_data)
        except:
            data['error'] = ['Not Found']
        return Response(data)


class StudentDashboardView(APIView):
    permission_classes = [IsAuthenticated, StudentPermission]

    def get(self, request):

        data = {}
        completed_quizes = Progress.objects.filter(
            student=request.user, is_completed=True)
        data['completed_quiz_list'] = []
        for completed_quiz in completed_quizes:
            data['completed_quiz_list'].append(
                ProgressSerializaer(instance=completed_quiz, context={"request": request}).data)

        in_progress_quizes = Progress.objects.filter(
            student=request.user, is_in_progress=True)

        data['in_progress_quiz_list'] = []
        for in_progress_quiz in in_progress_quizes:
            data['in_progress_quiz_list'].append(
                ProgressSerializaer(instance=in_progress_quiz, context={"request": request}).data)

        return Response(data)


class TimeRanOutView(APIView):
    permission_classes = [IsAuthenticated, StudentPermission]

    def get(self, request, category_pk):
        data = {}

        try:
            progress = Progress.objects.get(
                category__id=category_pk, student=request.user)
            progress.is_completed = True
            progress.is_in_progress = False
            progress.save()
            student_questions = StudentQuestion.objects.filter(
                student=request.user, question__category__id=category_pk).values_list('question')
            questions = Question.objects.filter(
                category__id=category_pk).exclude(id__in=student_questions)

            for question in questions:
                StudentQuestion.objects.create(
                    student=request.user, question=question, is_attempted=True, is_correct=False)
            data['message'] = ["Time's Up!"]
        except Progress.DoesNotExist:
            data['error'] = ['Not Found']

        return Response(data)


class GetLeaderBoardView(ListAPIView):
    permission_classes = [IsAuthenticated, TeacherPermission]
    serializer_class = ProgressSerializaer

    def get_queryset(self, *args, **kwargs):
        category_pk = self.kwargs['category_pk']
        return Progress.objects.filter(category__id=category_pk, is_completed=True).order_by('-marks')
