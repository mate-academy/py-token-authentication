from django.contrib.auth import get_user_model
from rest_framework import serializers

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    # дозволяємо оновлення пароля; не віддаємо його в GET
    password = serializers.CharField(
        write_only=True, min_length=5, required=False
    )

    class Meta:
        model = User
        fields = ("id", "username", "email", "is_staff", "password")
        read_only_fields = ("id", "is_staff")

    def update(self, instance, validated_data):
        password = validated_data.pop("password", None)
        user = super().update(instance, validated_data)
        if password:
            user.set_password(password)
            user.save(update_fields=["password"])
        return user


class UserRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "username", "email", "password")
        read_only_fields = ("id",)
        extra_kwargs = {"password": {"write_only": True, "min_length": 5}}

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)
