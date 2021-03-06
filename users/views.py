from django.shortcuts import render, get_object_or_404
from rest_framework.views import APIView
from .serializers import SignUpSerializer, LogInSerializer
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from .models import User
# Create your views here.


class SignUpView(APIView):
    permission_classes = []

    def post(self, request):
        serializer = SignUpSerializer(data=request.data)
        data = {}
        if serializer.is_valid():
            user = serializer.save()
            data['success'] = 'Successfully registered the user'
            data['username'] = user.username
            token = Token.objects.get(user=user).key
            data['token'] = token
        else:
            data = serializer.errors
        return Response(data)


class LogInView(APIView):
    permission_classes = []

    def post(self, request):
        serializer = LogInSerializer(data=request.data)
        data = {}
        if serializer.is_valid():
            validated_data = serializer.validated_data
            user = get_object_or_404(User, email=validated_data['email'])
            data['token'] = get_object_or_404(Token, user=user).key
            data['user_type'] = user.role
        else:
            data = serializer.errors
        return Response(data)
