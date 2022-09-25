from .models import Account, Replenishment, Transfer
from django.db import transaction


def get_user_accounts(user):
    return Account.objects.filter(user=user)


def get_user_replenishments(user):
    return Replenishment.objects.filter(account__in=get_user_accounts(user))


def get_transfers_from_user(user):
    return Transfer.objects.filter(from_account__in=get_user_accounts(user))


def get_transfers_to_user(user):
    return Transfer.objects.filter(to_account__in=get_user_accounts(user))


def get_all_user_transfers(user):
    return get_transfers_from_user(user).union(get_transfers_to_user(user))


def make_replenishment(account, amount):
    with transaction.atomic():
        account.balance += amount
        account.save()


def make_transfer(from_account, to_account, amount):
    with transaction.atomic():
        from_balance = from_account.balance - amount
        from_account.balance = from_balance
        from_account.save()

        to_balance = to_account.balance + amount
        to_account.balance = to_balance
        to_account.save()
