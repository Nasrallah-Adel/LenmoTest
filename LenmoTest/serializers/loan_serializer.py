from rest_framework import serializers
from rest_framework.fields import SerializerMethodField

from LenmoTest.serializers.offer_serializer import OfferSerializer
from db.models import Loan, Offer


class LoanSerializer(serializers.ModelSerializer):
    offers = SerializerMethodField()
    class Meta:
        model = Loan
        fields = ('id', 'amount', 'period', 'user', 'status', 'offers')
        read_only_fields = ('id', 'status', 'user')

    def get_offers(self, obj):
        offers = Offer.objects.filter(loan=obj.id   )
        data = []
        for offer in offers:
            dat = OfferSerializer(offer).data
            data.append(dat)
        return data
