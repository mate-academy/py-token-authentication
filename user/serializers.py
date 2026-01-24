from django.contrib.auth import get_user_model, authenticate

from rest_framework import serializers
from rest_framework.exceptions import ValidationError


User = get_user_model()


class UserRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=5)

    class Meta:
        model = User
        fields = ("id", "username", "password", "email")

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        user = authenticate(
            username=attrs.get("username"),
            password=attrs.get("password"),
        )
        if not user:
            raise serializers.ValidationError(
                "Unable to authenticate with provided credentials"
            )
        attrs["user"] = user
        return attrs


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True,
        required=False,
        min_length=5
    )

    class Meta:
        model = User
        fields = ("id", "username", "email", "password", "is_staff")
        read_only_fields = ("is_staff",)

    def update(self, instance, validated_data):
        password = validated_data.pop("password", None)
        user = super().update(instance, validated_data)

        if password:
            user.set_password(password)
            user.save()

        return user
