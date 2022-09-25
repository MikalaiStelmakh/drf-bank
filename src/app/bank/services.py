from .models import Account, Replenishment
from django.db import transaction


def get_user_accounts(user):
    return Account.objects.filter(user=user)


def get_user_replenishments(user):
    return Replenishment.objects.filter(account__in=get_user_accounts(user))


def make_replenishment(account, amount):
    with transaction.atomic():
        account.balance += amount
        account.save()
