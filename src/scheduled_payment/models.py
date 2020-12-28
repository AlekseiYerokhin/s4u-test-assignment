import datetime
import json
from decimal import Decimal

from django.db import models
from django.core.serializers.json import DjangoJSONEncoder

from account.models import Account
from transfer.models import Transfer

choices = [(i + 1, str(i + 1)) for i in range(0, 31)]


class ScheduledPayment(models.Model):
    day_of_payment = models.IntegerField(
        'Day Of Month',
        choices=choices
    )
    from_account = models.ForeignKey(
        'account.Account',
        null=True,
        on_delete=models.SET_NULL,
        related_name='from_account'
    )
    to_account = models.ForeignKey(
        'account.Account',
        null=True,
        on_delete=models.SET_NULL,
        related_name='to_account'
    )
    amount = models.DecimalField(max_digits=18, decimal_places=2)

    def is_payable(self):
        today = datetime.datetime.today()
        return self.day_of_payment == today.day

    def make_transaction(self):
        transfer = Transfer.do_transfer(
                from_account=self.from_account,
                to_account=self.to_account,
                amount=self.amount,
            )
        return transfer
