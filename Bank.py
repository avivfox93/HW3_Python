from datetime import date as dt


def _transfer_decorator(func):
    def inner(self, amount, to):
        old = self.balance
        res = func(self, amount, to)
        if res:
            print(
                'Date: {}, Name: {}, Number: {}, Old Balance: {}, Amount: {}, To: {}'.format(str(dt.today()), self.name,
                                                                                             self.num, old,
                                                                                             amount, to.name))
        return res
    return inner


def _action_decorator(func):
    def inner(self, amount):
        old = self.balance
        res = func(self, amount)
        if res:
            print('Date: {}, Name: {}, Number: {}, Old Balance: {}, {} Amount: {}'.format(str(dt.today()), self.name,
                                                                                          self.num, old,
                                                                                          func.__name__, amount))
        return res
    return inner


def balance_generator(accounts):
    for account in accounts:
        yield account.balance


class Account:

    def __init__(self, name, num, balance=0, credit=1500):
        self.name = name
        self.num = num
        self.balance = balance
        self.credit = credit

    def __str__(self):
        return str(self.name)

    @_action_decorator
    def withdrawal(self, amount):
        if (self.balance - amount) < (-self.credit):
            return False
        self.balance -= amount
        return True

    @_action_decorator
    def deposit(self, amount):
        self.balance += amount
        return True

    @_transfer_decorator
    def transfer(self, amount, to):
        if (self.balance - amount) < (-self.credit):
            return False
        self.balance -= amount
        to.deposit(amount)
        return True

