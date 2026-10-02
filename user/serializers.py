"""Registration and profile serialization with safe password handling."""
from __future__ import annotations

from typing import Any

from django.contrib.auth import get_user_model
from rest_framework import serializers

from user.models import User


class UserSerializer(serializers.ModelSerializer):
    """Never expose passwords or allow clients to assign staff privileges."""

    class Meta:
        model = get_user_model()
        fields: tuple[str, ...] = (
            "id", "username", "email", "password", "is_staff",
        )
        read_only_fields: tuple[str, ...] = ("id", "is_staff")
        extra_kwargs = {
            "password": {
                "write_only": True,
                "min_length": 5,
                "trim_whitespace": False,
            },
        }

    def create(self, validated_data: dict[str, Any]) -> User:
        return get_user_model().objects.create_user(**validated_data)

    def update(
        self, instance: User, validated_data: dict[str, Any]
    ) -> User:
        password = validated_data.pop("password", None)
        for attribute, value in validated_data.items():
            setattr(instance, attribute, value)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance
