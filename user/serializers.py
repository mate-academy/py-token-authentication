from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractBaseUser
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ("id", "username", "email", "password", "is_staff")
        read_only_fields = ("id", "is_staff")
        extra_kwargs = {
            "password": {
                "write_only": True,
                "min_length": 5,
                "trim_whitespace": False,
            },
        }

    def create(self, validated_data: dict) -> AbstractBaseUser:
        return get_user_model().objects.create_user(**validated_data)

    def update(
        self, instance: AbstractBaseUser, validated_data: dict
    ) -> AbstractBaseUser:
        password = validated_data.pop("password", None)
        for attribute, value in validated_data.items():
            setattr(instance, attribute, value)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance
