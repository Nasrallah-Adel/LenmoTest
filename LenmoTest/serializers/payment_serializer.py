from rest_framework import serializers

from db.models import LoanPayments


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = LoanPayments
        fields = ('id', 'amount', 'status', 'loan', 'offer', 'due_date')
        read_only_fields = ('id', 'status', 'user')
