from decimal import Decimal
from django.db import models
from account.models import Account


class InsufficientBalance(Exception):
    pass


class SameAccountsOperationException(Exception):
    pass


class UnacceptableTransferAmount(Exception):
    pass


class Transfer(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    from_account = models.ForeignKey(Account, models.CASCADE, related_name='transfers_in')
    to_account = models.ForeignKey(Account, models.CASCADE, related_name='transfers_out')
    amount = models.DecimalField(max_digits=18, decimal_places=2)

    @staticmethod
    def do_transfer(from_account: Account, to_account: Account, amount: Decimal):
        if from_account.balance < amount:
            raise InsufficientBalance()

        if from_account.number == to_account.number:
            raise SameAccountsOperationException()

        if amount < 0:
            raise UnacceptableTransferAmount()

        from_account.balance -= amount
        to_account.balance += amount

        from_account.save()
        to_account.save()

        return Transfer.objects.create(
            from_account=from_account,
            to_account=to_account,
            amount=amount
        )


"""
Extension suggestions:
For cash operations i would suggest just another Django app but as a POC at first time. 
For external operations it seems like it is better to implement a microservice due to it will to handle operations 
between different banks and therefore different APIs.
"""