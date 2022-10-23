from django.utils import timezone
import uuid
from django.db import models
from django.conf import settings
from django.db.models.query import Q, F


class BaseModel(models.Model):
    """
    Abstract base model that provides uuid primary key
    and created_at timestamp.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    created_at = models.DateTimeField(db_index=True, default=timezone.now)

    class Meta:
        abstract = True


class Customer(BaseModel):
    fname = models.CharField(verbose_name="First name", max_length=255)
    lname = models.CharField(verbose_name="Second name", max_length=255)
    city = models.CharField(max_length=255)

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )

    def __str__(self):
        return f'{self.fname} {self.lname}'


class Account(BaseModel):
    balance = models.DecimalField(

        default=0,
        max_digits=10,
        decimal_places=2
    )

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT  # we cannot delete user with money
    )

    class Meta:
        constraints = [
            models.CheckConstraint(
                name="negative_balance",
                check=Q(balance__gte=0)
            )
        ]

    def __str__(self):
        return f'Account {self.id} of {self.user.username}'


class Replenishment(BaseModel):
    amount = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    account = models.ForeignKey(
        Account,
        on_delete=models.CASCADE,
        related_name="replenishments"
    )

    class Meta:
        constraints = [
            models.CheckConstraint(
                name="negative_amount_replenishment",
                check=Q(amount__gte=0)
            )
        ]

    def __str__(self):
        return (
            f'{self.created_at}: '
            f'Account {self.account.id} of {self.account.user.username} '
            f'was replenished by {self.amount}')


class Transfer(BaseModel):
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

    class Meta:
        constraints = [
            models.CheckConstraint(
                name="negative_amount_transfer",
                check=Q(amount__gte=0)
            ),
            models.CheckConstraint(
                name="same_account_transfer",
                check=~Q(from_account__exact=F("to_account"))
            )
        ]

    def __str__(self):
        return (
            f'{self.created_at}: Transfer '
            f'from account {self.from_account.id} '
            f'to account {self.to_account.id} '
            f'for {self.amount}')
