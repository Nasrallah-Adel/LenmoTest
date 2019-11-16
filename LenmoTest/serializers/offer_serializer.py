from rest_framework import serializers

from db.models import Offer


class OfferSerializer(serializers.ModelSerializer):
    class Meta:
        model = Offer
        fields = ('id', 'interest_rate', 'loan', 'status', 'user')
        read_only_fields = ('id', 'status', 'user')


class AcceptOfferSerializer(serializers.ModelSerializer):
    class Meta:
        model = Offer
        fields = ('id', 'interest_rate', 'loan', 'status', 'user')
        read_only_fields = ('status', 'interest_rate', 'loan', 'user')
