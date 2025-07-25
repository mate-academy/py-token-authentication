from rest_framework import serializers
from django.contrib.auth import get_user_model

User = get_user_model()


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=5)

    class Meta:
        model = User
        fields = ("id", "username", "password")

    def create(self, validated_data):
        return User.objects.create_user(
            username=validated_data["username"],
            password=validated_data["password"]
        )


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "username", "email", "is_staff")
