from rest_framework import status
from rest_framework.exceptions import APIException
from rest_framework.generics import CreateAPIView, UpdateAPIView, ListAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import BasePermission
from rest_framework.response import Response

from rest_framework_jwt.authentication import JSONWebTokenAuthentication

from LenmoTest.serializers.loan_serializer import LoanSerializer
from LenmoTest.serializers.offer_serializer import OfferSerializer
from LenmoTest.serializers.user_serializer import UserBalanceSerializer

from db.models import User, Loan, Offer


class IsInvestor(BasePermission):
    """
    Allows access only to Investor  users.
    """

    def has_permission(self, request, view):
        return bool(request.user.is_authenticated and request.user.type == User.ACCOUNT_TYPE_INVESTOR)


class AuthenticationMixin(object):
    permission_classes = (IsInvestor,)
    authentication_classes = (JSONWebTokenAuthentication,)


class Error(APIException):
    status_code = 200
    default_detail = 'Sorry Can not create offer  , Loan already  Funded'


class OfferCreate(AuthenticationMixin, CreateAPIView):
    """
    two fields \n
    1- interest_rate : will be Annual Interest Rate \n
    2- loan : is will be " loan id " you can get it from "loans" Api
    """
    serializer_class = OfferSerializer

    def perform_create(self, serializer):
        serializer.validated_data['user'] = self.request.user
        loan_id = serializer.validated_data['loan']

        loan = Loan.objects.get(id=loan_id.id)

        if loan.status == Loan.LOAN_STATUS_FUNDED:
            raise Error
        serializer.save()


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 20
    last_page_strings = ('last',)


class LoanList(AuthenticationMixin, ListAPIView):
    """
        get all loans list and it is support pagination every page contain 20 item
        \n
        item will content of loan properties and offers of every loan
        """
    serializer_class = LoanSerializer
    pagination_class = StandardResultsSetPagination
    authentication_classes = (JSONWebTokenAuthentication,)
    queryset = Loan.objects.all()


class OfferList(AuthenticationMixin, ListAPIView):
    """
        get all loans list and it is support pagination every page contain 20 item
        \n
        item will content of loan properties and offers of every loan
        """
    serializer_class = OfferSerializer
    pagination_class = StandardResultsSetPagination
    authentication_classes = (JSONWebTokenAuthentication,)
    queryset = Offer.objects.all()


class DepositMoney(AuthenticationMixin, UpdateAPIView):
    """
        one field \n
        balance : to add balance to your account

        """

    serializer_class = UserBalanceSerializer
    queryset = User.objects.all()

    def put(self, request, *args, **kwargs):
        return self.patch(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        amount = request.data['balance']
        try:
            user = User.objects.get(id=request.user.id)
        except Exception as e:
            return Response(data={'message': 'user not exist  ' + str(e)})
        try:
            user.balance = user.balance + int(amount)
            user.save()
        except Exception as e:
            print(e)
            return Response(data={'message': ' error :  ' + str(e)})

        return Response(data={'message': 'Your New Balance Is ' + str(user.balance)})
