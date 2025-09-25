# write your code here
from django.contrib.auth import get_user_model
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ("id", "username", "email", "password", "is_staff")
        read_only_fiedls = ("id", "is_staff")
        extra_kwargs = {
            "password": {"write_only": True, "min_length": 5}

        }

    def create(self, validated_data):
        """create user with encrypted password"""
        return get_user_model().objects.create_user(**validated_data)

    def update(self, instance, validated_data):
        """Update User with encrypted password"""
        password = validated_data("password", None)
        user = super().update(instance, validated_data)

        if password:
            user.set_password(password)
            user.save()

        return user
