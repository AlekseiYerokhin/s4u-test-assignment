from django.test import TestCase
from functools import partial

from account.models import Account
from customer.models import Customer
from transfer.models import Transfer, UnacceptableTransferAmount


class TransferTest(TestCase):
    def setUp(self):
        super(TransferTest, self).setUp()

        customer = Customer.objects.create(
            email='test@test.invalid',
            full_name='Test Customer',
        )

        self.account1 = Account.objects.create(number=123, owner=customer, balance=1000)
        self.account2 = Account.objects.create(number=456, owner=customer, balance=1000)
        self.bound_accs_do_transfer = partial(Transfer.do_transfer, self.account1, self.account2)

    def test_basic_transfer(self):
        self.bound_accs_do_transfer(100)

        self.assertEqual(self.account1.balance, 900)
        self.assertEqual(self.account2.balance, 1100)
        self.assertTrue(Transfer.objects.filter(
            from_account=self.account1,
            to_account=self.account2,
            amount=100,
        ).exists())

    def test_transfer_unacceptable_amount(self):
        bound_negative_amount_transfer = partial(self.bound_accs_do_transfer, -100)

        self.assertRaises(UnacceptableTransferAmount, bound_negative_amount_transfer)