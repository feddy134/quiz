from django.shortcuts import render
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from .permissions import TeacherPermission

# Create your views here.


class IndexAPIView(APIView):
    permission_classes = [IsAuthenticated, TeacherPermission]

    def get(self, request):
        data = {}
        data['message'] = 'Yo'

        return Response(data)
    # queryset = Category.objects.order_by('id')
    # serializer_class = CategorySerializer
