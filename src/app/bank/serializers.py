from rest_framework import serializers, exceptions as rest_exceptions

from .models import Customer, Account, Replenishment, Transfer

from .services import make_replenishment, make_transfer


class CustomerSerializer(serializers.ModelSerializer):
    date_created = serializers.SerializerMethodField()

    class Meta:
        model = Customer
        fields = ('id', 'date_created', 'fname', 'lname', 'city', )
        read_only_fields = ('id', )

    def create(self, validated_data):
        # override standard method to create customer using put method
        validated_data['user_id'] = self.context['request'].user.id
        return super(CustomerSerializer, self).create(validated_data)

    def get_date_created(self, obj):
        # get date created as read only field
        return obj.user.date_joined.date()


class AccountSerializer(serializers.ModelSerializer):
    replenishments = serializers.PrimaryKeyRelatedField(
        many=True,
        read_only=True
    )

    class Meta:
        model = Account
        fields = ('id', 'balance', 'replenishments', )
        read_only_fields = ('id', 'balance', 'replenishments', )


class AccountOwnerForeignKey(serializers.PrimaryKeyRelatedField):
    def get_queryset(self):
        user = self.context['request'].user
        return Account.objects.filter(user=user)


class ReplenishmentSerializer(serializers.ModelSerializer):
    account = AccountOwnerForeignKey()

    class Meta:
        model = Replenishment
        fields = ('id', 'time_replenished', 'amount', 'account')
        read_only_fields = ('id', 'time_replenished', )

    def create(self, validated_data):
        make_replenishment(**validated_data)
        return super().create(validated_data)

    def validate_amount(self, value):
        if value <= 0:
            raise rest_exceptions.ValidationError(
                "Only positive amount of money can be provided."
            )
        return value


class TransferSerializer(serializers.ModelSerializer):
    from_account = AccountOwnerForeignKey()

    class Meta:
        model = Transfer
        fields = (
            'id',
            'time_transfered',
            'from_account',
            'to_account',
            'amount',
        )
        read_only_fields = ('id', 'time_transfered', )

    def create(self, validated_data):
        make_transfer(**validated_data)
        return super().create(validated_data)

    def validate_amount(self, value):
        if value <= 0:
            raise rest_exceptions.ValidationError(
                "Only positive amount of money can be provided."
            )
        return value

    def validate(self, attrs):
        if attrs['from_account'] == attrs['to_account']:
            raise rest_exceptions.ValidationError(
                {"to_account": "Choose another account."}
            )
        if attrs['amount'] > attrs['from_account'].balance:
            raise rest_exceptions.ValidationError(
                {"amount": "Not enough money."}
            )
        return attrs
