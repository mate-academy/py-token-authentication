from django.contrib.auth import get_user_model
from django.core.validators import MinLengthValidator
from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

User = get_user_model()


class RegisterUserSerializer(ModelSerializer):
    password = serializers.CharField(
        write_only=True, validators=[MinLengthValidator(5)]
    )

    class Meta:
        model = User
        fields = ["id", "username", "email", "password", "is_staff"]
        read_only_fields = ["id", "is_staff"]

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)

    def update(self, instance, validated_data):
        password = validated_data.pop("password")
        user = super().update(instance, validated_data)
        if password:
            user.set_password(password)
            user.save()
        return user
