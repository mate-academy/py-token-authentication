from rest_framework import serializers

from user.models import (
    User
)


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "username", "email", "password", "is_staff")
        read_only_fields = ("id", "is_staff")
        extra_kwargs = {
            "password": {
                "write_only": True,
            }
        }

    def validate_password(self, value):
        if len(value) < 5:
            raise serializers.ValidationError(
                "Password must be at least 5 characters."
            )
        return value

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)

    def update(self, instance, validated_data):
        instance.username = validated_data.get("username", instance.username)
        instance.email = validated_data.get("email", instance.email)
        instance.password = validated_data.get("password", instance.password)
        instance.set_password(instance.password)
        instance.save()
        return instance
