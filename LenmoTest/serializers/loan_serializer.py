from rest_framework import serializers
from rest_framework.fields import SerializerMethodField

from LenmoTest.serializers.offer_serializer import OfferSerializer
from LenmoTest.serializers.payment_serializer import PaymentSerializer
from db.models import Loan, Offer, LoanPayments


class LoanSerializer(serializers.ModelSerializer):
    offers = SerializerMethodField()
    payments = SerializerMethodField()

    class Meta:
        model = Loan
        fields = ('id', 'amount', 'period', 'user', 'status', 'offers', 'payments')
        read_only_fields = ('id', 'status', 'user', 'offers', 'payments')

    def get_offers(self, obj):
        request = self.context.get("request")
        offers = Offer.objects.filter(loan=obj.id, loan__user=request.user)
        data = []
        for offer in offers:
            dat = OfferSerializer(offer).data
            data.append(dat)
        return data

    def get_payments(self, obj):
        request = self.context.get("request")
        payments = LoanPayments.objects.filter(loan=obj.id, loan__user=request.user)
        data = []
        for payment in payments:
            dat = PaymentSerializer(payment).data
            data.append(dat)
        return data


