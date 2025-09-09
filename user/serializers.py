from django.contrib.auth import get_user_model
from rest_framework import serializers

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "username", "email", "password", "is_staff",)
        read_only_fields = ("id", "is_staff",)
        extra_kwargs = {"password": {"write_only": True, "min_length": 5}}

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)

    def update(self, instance, validated_data):
        username = validated_data.pop("username", instance.username)
        email = validated_data.pop("email", instance.email)
        password = validated_data.pop("password", None)

        instance.username = username
        instance.email = email

        if password:
            instance.set_password(password)

        instance.save()

        return instance
