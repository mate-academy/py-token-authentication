from django.contrib.auth import get_user_model
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = (
            "id",
            "username",
            "email",
            "is_staff",
        )
        read_only_fields = (
            "id",
            "is_staff",
        )


class UserCreateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        min_length=5,
        write_only=True,
        trim_whitespace=False,
    )

    class Meta:
        model = get_user_model()
        fields = (
            "id",
            "username",
            "password",
        )

    def create(self, validated_data):
        return get_user_model().objects.create_user(
            **validated_data
        )
