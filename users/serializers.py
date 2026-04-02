from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from .models import CustomUser 
from django.contrib.auth import authenticate

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=6)

    class Meta:
        model = CustomUser
        fields = ["email", "username", "password"]

    def create(self, validated_data):
        user = CustomUser(
            email=validated_data['email'],
            username=validated_data['username']
        )
        user.set_password(validated_data['password'])  # ✅ hash password
        user.save()
        return user
    


class LoginSerializer(TokenObtainPairSerializer):
    username_field = "email"  # 🔥 tells JWT to use email

    def validate(self, attrs):
        email = attrs.get("email")
        password = attrs.get("password")

        user = authenticate(request=self.context.get("request"), email=email, password=password)

        if not user:
            raise serializers.ValidationError("Invalid email or password")

        data = super().validate(attrs)
        return data