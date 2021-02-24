from rest_framework import serializers
from .models import User
from rest_framework.authtoken.models import Token
from .utils import name_to_first_name_and_last_name
from django.contrib.auth import authenticate


class SignUpSerializer(serializers.ModelSerializer):

    password2 = serializers.CharField(style={'input_type': 'password'})

    class Meta:
        model = User
        fields = ['email', 'username', 'role', 'password', 'password2']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def save(self):
        password = self.validated_data['password']
        password2 = self.validated_data['password2']

        if password != password2:
            raise serializers.ValidationError(
                {'password': 'Passwords must match'})

        first_name, last_name = name_to_first_name_and_last_name(
            self.validated_data['username'])

        user = User(
            username=self.validated_data['username'], email=self.validated_data['email'], role=self.validated_data['role'], first_name=first_name, last_name=last_name)
        user.set_password(password)

        user.save()
        Token.objects.create(user=user)
        return user


class LogInSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()

    def validate(self, attrs):
        validated_data = super().validate(attrs)
        email = validated_data['email']
        password = validated_data['password']

        if email and password:
            user = authenticate(email=email, password=password)
            if user is None:
                raise serializers.ValidationError(
                    {'error': 'Invalid Credentials'})
        return validated_data
