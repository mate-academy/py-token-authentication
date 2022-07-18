from django.contrib.auth import get_user_model
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ("id", "username", "email", "password", "is_staff")
        read_only_fields = ("id", "is_staff")
        extra_kwargs = {
            "password": {
                "write_only": True,
                "min_length": 5,
            }
        }

    def create(self, validated_data):
        """
        Create user with encrypted password
        """
        return get_user_model().objects.create_user(**validated_data)

    def update(self, instance, validated_data):
        password = validated_data.pop("password", None)

        for (key, value) in validated_data.items():
            setattr(instance, key, value)

        if password:
            instance.set_password(password)
            instance.save()

        return instance
