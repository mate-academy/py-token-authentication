from typing import Any

from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractBaseUser

from rest_framework.serializers import ModelSerializer


class UserSerializer(ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = [
            "id",
            "username",
            "email",
            "password",
            "is_staff",
        ]
        read_only_fields = [
            "id",
            "is_staff",
        ]
        extra_kwargs = {
            "password": {
                "write_only": True,
                "min_length": 5
            }
        }

    def create(
        self,
        validated_data: dict[str, Any]
    ) -> AbstractBaseUser:
        return get_user_model().objects.create_user(
            **validated_data
        )

    def update(
        self,
        instance: AbstractBaseUser,
        validated_data: dict[str, Any]
    ) -> AbstractBaseUser:
        password = validated_data.pop("password", None)
        user = super().update(instance, validated_data)

        if password is not None:
            user.set_password(password)
            user.save(update_fields=["password"])

        return user
