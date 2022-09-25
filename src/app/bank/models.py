import uuid
from django.db import models
from django.conf import settings


class Customer(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    fname = models.CharField(verbose_name="First name", max_length=255)
    lname = models.CharField(verbose_name="Second name", max_length=255)
    city = models.CharField(max_length=255)

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )

    def __str__(self):
        return f'{self.fname} {self.lname}'


class Account(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    balance = models.DecimalField(

        default=0,
        max_digits=10,
        decimal_places=2
    )

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT  # we cannot delete user with money
    )

    def __str__(self):
        return f'Account {self.id} of {self.user.username}'


class Replenishment(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    amount = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    account = models.ForeignKey(
        Account,
        on_delete=models.CASCADE,
        related_name="replenishments"
    )

    time_replenished = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return (
            f'{self.date_replenished}: '
            f'Account {self.account.id} of {self.account.user.username} '
            f'was replenished by {self.amount}')


class Transfer(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    from_account = models.ForeignKey(
        Account,
        on_delete=models.CASCADE,
        related_name='from_account'
    )

    to_account = models.ForeignKey(
        Account,
        on_delete=models.CASCADE,
        related_name='to_account'
    )

    amount = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    time_transfered = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return (
            f'{self.date_transfered}: Transfer '
            f'from account {self.from_account.id} '
            f'to account {self.to_account.id}')
