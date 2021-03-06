from django.urls import path, include
from .views import (CategoryListView, CreateCategoryView, CreateQuestionView,
                    QuestionListView, QuestionDetailsView, ProgressByCategoryListView,
                    CategoriesByAuthorView, AttendQuizView, ResultView, StudentDashboardView,
                    TimeRanOutView, GetLeaderBoardView)

urlpatterns = [

    path('create-category/', CreateCategoryView.as_view(), name='create_category'),
    path('question-list/<uuid:category_pk>/',
         QuestionListView.as_view(), name='question_list'),
    path('question-detail/<uuid:question_pk>/',
         QuestionDetailsView.as_view(), name='question_detail'),
    path('create-question/<uuid:category_pk>/',
         CreateQuestionView.as_view(), name='create_question'),
    path('progress-list/<uuid:category_pk>/',
         ProgressByCategoryListView.as_view(), name='progress_list'),
    path('categories-list-by-author/',
         CategoriesByAuthorView.as_view(), name='categories_list_by_author'),


    path('student-dashboard/', StudentDashboardView.as_view(),
         name='student_dashboard'),
    path('category-list/', CategoryListView.as_view(), name='category_list'),
    path('attend-quiz/<uuid:category_pk>/',
         AttendQuizView.as_view(), name='attend_quiz'),
    path('result/<uuid:category_pk>/',
         ResultView.as_view(), name='progress_details'),
    path('time-ran-out/<uuid:category_pk>/',
         TimeRanOutView.as_view(), name='time_ran_out'),
    path('get-leaderboard/<uuid:category_pk>/',
         GetLeaderBoardView.as_view(), name='get-leaderboard'),

]
