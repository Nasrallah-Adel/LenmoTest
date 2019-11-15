from coreschema.formats import validate_email
from django.contrib.auth import authenticate
from django.contrib.auth.hashers import make_password

from django.utils.translation import ugettext_lazy as _

from rest_framework import serializers
from rest_framework.generics import get_object_or_404

from db.models import User


class AuthLoginSerializer(serializers.Serializer):
    email_or_phone = serializers.CharField(label=_("email_or_phone"))
    password = serializers.CharField(
        label=_("Password"),
        style={'input_type': 'password'},
        trim_whitespace=False
    )

    def validate(self, attrs):
        email_or_phone = attrs.get('email_or_phone')
        password = attrs.get('password')
        print(email_or_phone)
        print(password)
        passs = make_password(password, salt='pharma')
        if email_or_phone and password:
            if not validate_email(email_or_phone):
                user_request = get_object_or_404(
                    User,
                    phone=email_or_phone,
                )

                email_or_phone = user_request.email

            user = authenticate(email=email_or_phone, password=password)

            if not user:
                msg = _('Unable to log in with provided credentials.')
                raise serializers.ValidationError(msg, code='authorization')
        else:
            msg = _('Must include "email_or_phone" and "password".')
            raise serializers.ValidationError(msg, code='authorization')

        attrs['user'] = user
        return attrs
