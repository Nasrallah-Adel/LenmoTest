import datetime

from rest_framework.generics import CreateAPIView, ListAPIView, UpdateAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated, BasePermission
from rest_framework.response import Response
from rest_framework_jwt.authentication import JSONWebTokenAuthentication

from LenmoTest.FINAL_VALUES import *
from LenmoTest.serializers.loan_serializer import LoanSerializer
from LenmoTest.serializers.offer_serializer import AcceptOfferSerializer
from LenmoTest.serializers.user_serializer import UserBalanceSerializer
from db.models import Loan, Offer, User, LenmonProfit, LoanPayments


class IsBorrower(BasePermission):
    """
    Allows access only to Borrower  users.
    """

    def has_permission(self, request, view):
        return bool(request.user.is_authenticated and request.user.type == User.ACCOUNT_TYPE_BORROWER)


class AuthenticationMixin(object):
    permission_classes = (IsBorrower,)
    authentication_classes = (JSONWebTokenAuthentication,)


class LoanRequestCreate(AuthenticationMixin, CreateAPIView):
    """
you have two fields \n
 1 - amount : money you need for loan \n
 2 - period : related for number of month's you will pay back the loan amount
    """
    serializer_class = LoanSerializer

    def perform_create(self, serializer):
        serializer.validated_data['user'] = self.request.user
        serializer.save()


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 20
    last_page_strings = ('last',)


class LoanRequestList(AuthenticationMixin, ListAPIView):
    serializer_class = LoanSerializer
    pagination_class = StandardResultsSetPagination
    authentication_classes = (JSONWebTokenAuthentication,)

    def get_queryset(self):
        user = self.request.user
        qs = Loan.objects.filter(user=user).order_by('id')
        return qs


class AcceptOffer(AuthenticationMixin, UpdateAPIView):
    serializer_class = AcceptOfferSerializer
    queryset = Offer.objects.all()

    def put(self, request, *args, **kwargs):
        return self.patch(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        pk = request.data['offer_id']

        try:
            offer = Offer.objects.get(id=pk)
        except Exception as e:
            return Response(data={'message': 'The offer not  accepted because not exist : ' + str(e)})

        if offer.loan.user == request.user:
            if offer.status == Offer.OFFER_STATUS_ACCEPTED:
                return Response(data={'message': 'The offer has already been accepted at : ' + str(offer.updated_at)})
            if offer.user.balance < offer.loan.amount + LENMO_PROFIT:
                return Response(data={'message': "offer Not Accepted ,Investor Don't Have Money Yet Sorry Try Later "})
            investor = User.objects.get(id=offer.user.id)
            investor.balance = investor.balance - offer.loan.amount - LENMO_PROFIT
            investor.save()
            borrower = User.objects.get(id=offer.loan.user.id)
            borrower.balance = borrower.balance + offer.loan.amount
            loan = Loan.objects.get(id=offer.loan.id)
            loan.status = Loan.LOAN_STATUS_FUNDED
            loan.save()
            offer.status = Offer.OFFER_STATUS_ACCEPTED
            offer.save()

            borrower.save()
            self.make_LoanPayments(loan, offer)
            LenmonProfit(offer=offer, loan=offer.loan, profit=LENMO_PROFIT).save()

            return Response(data={'message': 'offer Accepted  successfully'})

        return Response(data={'message': 'offer Not Accepted ,Not Belong to You'})

    def make_LoanPayments(self, loan, offer):

        daily_interest = ((loan.amount * (offer.interest_rate / 100.0))) / (365)
        monthely_interest = daily_interest * 30
        all_interest = monthely_interest * loan.period

        amount = (all_interest + loan.amount) / loan.period
        today = datetime.datetime.now()

        # today = today.strftime("%Y-%m-%d")
        due_date = today + datetime.timedelta(days=30)

        for _ in range(loan.period):
            LoanPayments(offer=offer, loan=loan, amount=amount, due_date=due_date).save()
            due_date = due_date + datetime.timedelta(days=30)


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
