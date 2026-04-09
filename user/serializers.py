from django.contrib.auth import get_user_model
from rest_framework import serializers


USER_MODEL = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = USER_MODEL
        fields = ("id", "username", "email", "password", "is_staff")
        read_only_fields = ("id", "is_staff")
        extra_kwargs = {
            "password": {
                "write_only": True,
                "min_length": 5
            }
        }

    def create(self, validated_data: dict) -> USER_MODEL:
        return USER_MODEL.objects.create_user(**validated_data)

    def update(
        self,
        instance: USER_MODEL,
        validated_data: dict
    ) -> USER_MODEL:
        password = validated_data.pop("password", None)
        user = super().update(instance, validated_data)

        if password:
            user.set_password(password)
            user.save()

        return user
