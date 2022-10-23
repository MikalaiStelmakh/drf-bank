from rest_framework import generics, viewsets, mixins
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from .models import Customer, Account, Replenishment, Transfer
from .serializers import (
    CustomerSerializer,
    AccountSerializer,
    ReplenishmentSerializer,
    TransferSerializer
)
from .services import (
    get_user_accounts,
    get_user_replenishments,
    get_all_user_transfers,
)


class CustomerDetail(generics.RetrieveUpdateAPIView):
    serializer_class = CustomerSerializer
    authentication_classes = (TokenAuthentication, )
    permission_classes = (IsAuthenticated, )
    queryset = Customer.objects.all()

    def get_object(self):
        return self.queryset.filter(user=self.request.user).first()


class AccountView(viewsets.GenericViewSet,
                  mixins.ListModelMixin,
                  mixins.RetrieveModelMixin,
                  mixins.CreateModelMixin,
                  mixins.DestroyModelMixin):
    serializer_class = AccountSerializer
    authentication_classes = (TokenAuthentication, )
    permission_classes = (IsAuthenticated, )
    queryset = Account.objects.all()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_queryset(self):
        # View only accounts owned by logged in user.
        return get_user_accounts(self.request.user)


class ReplenishmentView(viewsets.GenericViewSet,
                        mixins.ListModelMixin,
                        mixins.RetrieveModelMixin,
                        mixins.CreateModelMixin):
    serializer_class = ReplenishmentSerializer
    authentication_classes = (TokenAuthentication, )
    permission_classes = (IsAuthenticated, )
    queryset = Replenishment.objects.all()

    def get_queryset(self):
        # View only replenishments on accounts
        # owned by logged in user.
        return get_user_replenishments(self.request.user)


class TransferView(viewsets.GenericViewSet,
                   mixins.ListModelMixin,
                   mixins.RetrieveModelMixin,
                   mixins.CreateModelMixin):
    serializer_class = TransferSerializer
    authentication_classes = (TokenAuthentication, )
    permission_classes = (IsAuthenticated, )
    queryset = Transfer.objects.all()

    def get_queryset(self):
        # View only transfers from or to accounts
        # owned by logged in user.
        return get_all_user_transfers(self.request.user)
