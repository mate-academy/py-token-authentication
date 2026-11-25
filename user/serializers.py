from rest_framework import serializers

from django.contrib.auth import get_user_model


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = (
            "id",
            "username",
            "password",
            "email",
            "is_staff"
        )
        extra_kwargs = {
            "password": {
                "write_only": True,
                "min_length": 5
            }
        }

    def create(self, validated_data):
        password = validated_data.pop("password")
        user = get_user_model().objects.create_user(
            **validated_data
        )
        user.set_password(password)
        user.save()
        return user

    def update(self, instance, validated_data):
        password = validated_data.pop("password", None)
        instance = super().update(
            instance=instance,
            validated_data=validated_data
        )
        if password:
            instance.set_password(password)
        instance.save()
        return instance
