from rest_framework import serializers

from user.models import User


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=5)
    is_staff = serializers.BooleanField(read_only=True)

    class Meta:
        model = User
        fields = ("id", "username", "email", "password", "is_staff")

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)

    def update(self, instance, validated_data):
        if "password" in validated_data:
            password = validated_data.pop("password")
            if password:
                instance.set_password(password)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance
