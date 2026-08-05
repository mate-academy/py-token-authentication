from django.contrib.auth import get_user_model
from rest_framework import serializers

from user.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "username", "email", "is_staff", "password")
        extra_kwargs = {
            "password": {"write_only": True, "min_length": 5},
            "is_staff": {"read_only": True},
        }

    def create(self, validated_data):
        return get_user_model().objects.create_user(**validated_data)

    def update(self, instance, validated_data):
        password = validated_data.pop("password", None)
        user = super().update(instance, validated_data)

        if password:
            user.set_password(password)
            user.save()

        return user
