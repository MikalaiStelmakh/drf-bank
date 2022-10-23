from .models import Account, Replenishment, Transfer
from users.models import User

from django.db.models.query import QuerySet
from django.db import transaction


def get_user_accounts(user: User) -> QuerySet[Account]:
    """Returns a queryset of all accounts owned by user."""
    return Account.objects.filter(user=user)


def get_user_replenishments(user: User) -> QuerySet[Replenishment]:
    """Returns a queryset of replenishments on all user accounts."""
    return Replenishment.objects.filter(account__in=get_user_accounts(user))


def get_transfers_from_user(user: User) -> QuerySet[Transfer]:
    """Returns a queryset of transfers from all user accounts."""
    return Transfer.objects.filter(from_account__in=get_user_accounts(user))


def get_transfers_to_user(user: User) -> QuerySet[Transfer]:
    """Returns a queryset of transfers to all user accounts."""
    return Transfer.objects.filter(to_account__in=get_user_accounts(user))


def get_all_user_transfers(user: User) -> QuerySet[Transfer]:
    """Returns a queryset of transfers from and to all user accounts."""
    return get_transfers_from_user(user).union(get_transfers_to_user(user))


def make_replenishment(account: Account, amount: float):
    """Replenishes the account with given amount."""
    with transaction.atomic():
        account.balance += amount
        account.save()


def make_transfer(from_account: Account, to_account: Account, amount: float):
    """Transfers given amount from from_account to to_account."""
    with transaction.atomic():
        from_balance = from_account.balance - amount
        from_account.balance = from_balance
        from_account.save()

        to_balance = to_account.balance + amount
        to_account.balance = to_balance
        to_account.save()
