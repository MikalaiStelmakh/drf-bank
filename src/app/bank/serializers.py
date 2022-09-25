from rest_framework import serializers
from .models import Customer, Account, Replenishment, Transfer


class CustomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ('id', 'fname', 'lname', 'city', )
        read_only_fields = ('id', )


class AccountSerializer(serializers.ModelSerializer):
    actions = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta:
        model = Account
        fields = ('id', 'balance', 'actions', )
        read_only_fields = ('id', 'balance', 'actions', )


class AccountOwnerForeignKey(serializers.PrimaryKeyRelatedField):
    def get_queryset(self):
        user = self.context['request'].user
        return Account.objects.filter(user=user)


class ReplenishmentSerializer(serializers.ModelSerializer):
    account = AccountOwnerForeignKey()

    class Meta:
        model = Replenishment
        fields = ('id', 'amount', 'account')
        # TODO: add replanishment date to
        read_only_fields = ('id', )


class TransferSerializer(serializers.ModelSerializer):
    from_account = AccountOwnerForeignKey()

    class Meta:
        model = Transfer
        fields = ('id', 'from_account', 'to_account', 'amount', )
        read_only_fields = ('id', )