from django.shortcuts import render
from rest_framework.generics import CreateAPIView, ListAPIView, UpdateAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_jwt.authentication import JSONWebTokenAuthentication

from LenmoTest.serializers.loan_serializer import LoanSerializer
from LenmoTest.serializers.offer_serializer import OfferSerializer, AcceptOfferSerializer
from db.models import Loan, Offer


class AuthenticationMixin(object):
    permission_classes = (IsAuthenticated,)
    authentication_classes = (JSONWebTokenAuthentication,)


class LoanRequestCreate(AuthenticationMixin, CreateAPIView):
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
    lookup_field = 'id'

    def put(self, request, *args, **kwargs):
        return self.patch(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        pk = kwargs['id']
        print(pk)
        offer = Offer.objects.get(id=pk)

        if offer.loan.user == request.user:
            if offer.status == Offer.OFFER_STATUS_ACCEPTED:
                return Response(data={'message': 'The offer has already been accepted at : ' + str(offer.updated_at)})
            if offer.user.balance < offer.loan.amount + 3:
                return Response(data={'message': "Investor Don't Have Money Yet Sorry Try Later "})

            offer.status = Offer.OFFER_STATUS_ACCEPTED
            offer.save()
            return Response(data={'message': 'offer Accepted  successfully'})

        return Response(data={'message': 'offer Not Accepted ,Not Belong to You'})
