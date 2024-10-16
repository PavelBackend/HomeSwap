from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken

User = get_user_model()

class RegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password')  # Включаем email в поля
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def validate_username(self, value):
        """Проверка уникальности имени пользователя."""
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError("Это имя пользователя уже занято.")
        return value

    def validate_email(self, value):
        """Проверка уникальности электронной почты."""
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("Этот email уже зарегистрирован.")
        return value

    def create(self, validated_data):
        """Создание нового пользователя с хэшированным паролем."""
        user = User(
            username=validated_data['username'],
            email=validated_data['email']  # Убедитесь, что email поддерживается в вашей модели
        )
        user.set_password(validated_data['password'])  # Хэшируем пароль
        user.save()
        return user