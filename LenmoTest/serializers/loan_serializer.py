from rest_framework import serializers

from db.models import Loan


class LoanSerializer(serializers.ModelSerializer):
    class Meta:
        model = Loan
        fields = ('id', 'amount', 'period', 'user', 'status')
        read_only_fields = ('id', 'status', 'user')
