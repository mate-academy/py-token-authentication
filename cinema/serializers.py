from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.authtoken.models import Token

User = get_user_model()

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ("username", "password", "email")

    def validate_password(self, value):
        # Regras: mínimo 5, máximo 55 (ajuste se quiser outro limite)
        if not value:
            raise serializers.ValidationError("A senha não pode ser vazia.")
        if len(value) < 5:
            raise serializers.ValidationError("A senha deve ter pelo menos 5 caracteres.")
        if len(value) > 55:
            raise serializers.ValidationError("A senha deve ter no máximo 55 caracteres.")
        return value

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data["username"],
            password=validated_data["password"],
            email=validated_data.get("email", ""),
        )
        Token.objects.get_or_create(user=user)
        return user
