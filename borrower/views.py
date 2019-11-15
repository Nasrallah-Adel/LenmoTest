from django.shortcuts import render
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework_jwt.authentication import JSONWebTokenAuthentication

from LenmoTest.serializers.loan_serializer import LoanSerializer


class AuthenticationMixin(object):
    permission_classes = (IsAuthenticated,)
    authentication_classes = (JSONWebTokenAuthentication,)


class LoanRequest(AuthenticationMixin, CreateAPIView):
    serializer_class = LoanSerializer

    def perform_create(self, serializer):
        serializer.validated_data['user'] = self.request.user
        serializer.save()
