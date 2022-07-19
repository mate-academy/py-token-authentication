from django.contrib.auth import get_user_model
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = get_user_model()
        fields = ("id", "username", "email", "password", "is_staff")
        read_only_fields = ("id", "is_staff")
        extra_kwargs = {"password": {"write_only": True, "min_length": 5}}

    def create(self, validated_date):
        return get_user_model().objects.create_user(**validated_date)

    def update(self, instance, validate_data):
        password = validate_data.pop("password", None)
        user = super().update(instance, validate_data)

        if password:
            user.set_password(password)
            user.save()

        return user

