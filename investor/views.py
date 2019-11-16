from django.shortcuts import render

# Create your views here.
from rest_framework.generics import CreateAPIView, UpdateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_jwt.authentication import JSONWebTokenAuthentication

from LenmoTest.serializers.offer_serializer import OfferSerializer
from LenmoTest.serializers.user_serializer import UserBalanceSerializer
from db.models import User


class AuthenticationMixin(object):
    permission_classes = (IsAuthenticated,)
    authentication_classes = (JSONWebTokenAuthentication,)


class OfferCreate(AuthenticationMixin, CreateAPIView):
    serializer_class = OfferSerializer

    def perform_create(self, serializer):
        serializer.validated_data['user'] = self.request.user
        serializer.save()



