from django.db import IntegrityError
from django.test import TestCase
from django.contrib.auth import get_user_model
from bank.models import Customer, Account, Transfer, Replenishment


def sample_user(email="test@test.com", password="testpass"):
    """Create a sample user"""
    return get_user_model().objects.create_user(email, password)


class ModelTest(TestCase):
    def test_customer_str(self):
        customer = Customer.objects.create(
            user=sample_user(),
            fname="John",
            lname="Doe",
            city="New York"
        )

        self.assertEqual(str(customer), f"{customer.fname} {customer.lname}")

    def test_account_negative_balance(self):
        user = sample_user()
        balance = -132

        with self.assertRaises(IntegrityError):
            Account.objects.create(
                user=user,
                balance=balance
            )

    def test_account_str(self):
        user = sample_user()
        account = Account.objects.create(
            user=user
        )

        self.assertEqual(str(account), f"Account {account.id} of {user.username}")

    def test_replenishment_negative_amount(self):
        user = sample_user()
        account = Account.objects.create(
            user=user
        )
        amount = -0.01

        with self.assertRaises(IntegrityError):
            Replenishment.objects.create(
                account=account,
                amount=amount
            )

    def test_replenishment_str(self):
        user = sample_user()
        account = Account.objects.create(
            user=user
        )
        amount = 100
        replenishment = Replenishment.objects.create(
            account=account,
            amount=amount
        )

        message = (
            f"{replenishment.created_at}: "
            f"Account {account.id} of {user.username} "
            f"was replenished by {amount}"
        )
        self.assertEqual(str(replenishment), message)

    def test_transfer_negative_amount(self):
        user1 = sample_user(email="test1@test.com", password="testpass")
        user2 = sample_user(email="test2@test.com", password="testpass")

        balance1 = 500
        balance2 = 0

        account1 = Account.objects.create(
            user=user1,
            balance=balance1
        )

        account2 = Account.objects.create(
            user=user2,
            balance=balance2
        )

        amount = -100

        with self.assertRaises(IntegrityError):
            Transfer.objects.create(
                from_account=account1,
                to_account=account2,
                amount=amount
            )

    def test_transfer_same_account(self):
        user = sample_user()

        balance1 = 500

        account = Account.objects.create(
            user=user,
            balance=balance1
        )

        amount = 321

        with self.assertRaises(IntegrityError):
            Transfer.objects.create(
                from_account=account,
                to_account=account,
                amount=amount
            )

    def test_transfer_str(self):
        user1 = sample_user(email="test1@test.com", password="testpass")
        user2 = sample_user(email="test2@test.com", password="testpass")

        balance1 = 500
        balance2 = 0

        account1 = Account.objects.create(
            user=user1,
            balance=balance1
        )

        account2 = Account.objects.create(
            user=user2,
            balance=balance2
        )

        amount = 321
        transfer = Transfer.objects.create(
            from_account=account1,
            to_account=account2,
            amount=amount
        )

        message = (
            f"{transfer.created_at}: Transfer "
            f"from account {account1.id} "
            f"to account {account2.id} "
            f"for {amount}"
        )

        self.assertEqual(str(transfer), message)

