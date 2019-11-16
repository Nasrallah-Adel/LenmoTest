from rest_framework.generics import CreateAPIView, UpdateAPIView
from rest_framework.permissions import BasePermission
from rest_framework.response import Response

from rest_framework_jwt.authentication import JSONWebTokenAuthentication

from LenmoTest.serializers.offer_serializer import OfferSerializer
from LenmoTest.serializers.user_serializer import UserBalanceSerializer

from db.models import User


class IsInvestor(BasePermission):
    """
    Allows access only to Investor  users.
    """

    def has_permission(self, request, view):
        return bool(request.user.is_authenticated and request.user.type == User.ACCOUNT_TYPE_INVESTOR)


class AuthenticationMixin(object):
    permission_classes = (IsInvestor,)
    authentication_classes = (JSONWebTokenAuthentication,)


class OfferCreate(AuthenticationMixin, CreateAPIView):
    serializer_class = OfferSerializer

    def perform_create(self, serializer):
        serializer.validated_data['user'] = self.request.user
        serializer.save()


class DepositMoney(AuthenticationMixin, UpdateAPIView):
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
