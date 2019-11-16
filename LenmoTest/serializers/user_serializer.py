from django.contrib.auth.hashers import make_password
from rest_framework import serializers

from db.models import User


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=False)

    class Meta:
        model = User
        fields = (
            'id', 'username', 'email', 'type', 'password', 'gender')

        read_only_fields = ('id',)

    def validate_email(self, email):
        return email.lower()

    def validate_password(self, password):
        if password:
            return make_password(password, salt='lenmo')


class UserBalanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'id', 'balance')

        read_only_fields = ('id',)


