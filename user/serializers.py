from typing import Any

from django.contrib.auth import get_user_model, authenticate
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ("id", "username", "email", "password", "is_staff")
        read_only_fields = ("id", "is_staff")
        extra_kwargs = {"password": {"write_only": True, "min_length": 5}}

    def create(self, validated_data: dict[str, Any]):
        return get_user_model().objects.create_user(**validated_data)

    def update(self, instance: Any, validated_data: dict[str, Any]) -> Any:
        password = validated_data.pop("password", None)
        user = super().update(instance, validated_data)

        if password:
            user.set_password(password)
            user.save()

        return user


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, attrs: dict[str, Any]) -> dict[str, Any]:
        username = attrs.get("username")
        password = attrs.get("password")

        user = authenticate(username=username, password=password)

        if not user:
            raise serializers.ValidationError({
                "non_field_errors": (
                    "Unable to authenticate with provided credentials."
                )
            })

        if not user.is_active:
            raise serializers.ValidationError({
                "non_field_errors": "User account is disabled."
            })

        attrs["user"] = user
        return attrs
