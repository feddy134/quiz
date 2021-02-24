from django.urls import path, include
from .views import IndexAPIView

urlpatterns = [
    path('', IndexAPIView.as_view(), name='api_index'),

]
