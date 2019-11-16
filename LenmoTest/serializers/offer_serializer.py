from rest_framework import serializers
from rest_framework.fields import SerializerMethodField

from db.models import Offer, Loan


class OfferSerializer(serializers.ModelSerializer):
    class Meta:
        model = Offer
        fields = ('id', 'interest_rate', 'loan', 'status', 'user')
        read_only_fields = ('id', 'status', 'user')


class AcceptOfferSerializer(serializers.Serializer):
    offer_id = serializers.IntegerField(required=True)

    class Meta:
        fields = ('offer_id',)
