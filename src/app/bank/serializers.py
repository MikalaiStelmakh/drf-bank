from rest_framework import serializers

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
        fields = ('id', 'created_at', 'balance', 'replenishments', )
        read_only_fields = ('id', 'created_at', 'balance', 'replenishments', )


class AccountOwnerForeignKey(serializers.PrimaryKeyRelatedField):
    def get_queryset(self):
        user = self.context['request'].user
        return Account.objects.filter(user=user)


class ReplenishmentSerializer(serializers.ModelSerializer):
    account = AccountOwnerForeignKey()

    class Meta:
        model = Replenishment
        fields = ('id', 'created_at', 'amount', 'account')
        read_only_fields = ('id', 'created_at', )

    def create(self, validated_data):
        make_replenishment(**validated_data)
        return super().create(validated_data)


class TransferSerializer(serializers.ModelSerializer):
    from_account = AccountOwnerForeignKey()

    class Meta:
        model = Transfer
        fields = (
            'id',
            'created_at',
            'from_account',
            'to_account',
            'amount',
        )
        read_only_fields = ('id', 'created_at', )

    def create(self, validated_data):
        make_transfer(**validated_data)
        return super().create(validated_data)
