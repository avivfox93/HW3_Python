from datetime import date as dt


def _transfer_decorator(func):
    def inner(self, amount, to):
        print('Date: {}, Name: {}, Number: {}, Old Balance: {}, Amount: {}, To: {}'.format(str(dt.today()), self.name, self.num, self.balance, amount, to.name))
        return func(self, amount, to)
    return inner


def _action_decorator(func):
    def inner(self, amount):
        print('Date: {}, Name: {}, Number: {}, Old Balance: {}, {} Amount: {}'.format(str(dt.today()), self.name, self.num, self.balance, func.__name__, amount))
        return func(self, amount)
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

    @_transfer_decorator
    def transfer(self, amount, to):
        print('b-a= {}, credit= {}'.format(self.balance-amount,-self.credit))
        if (self.balance - amount) < (-self.credit):
            return False
        self.balance -= amount
        to.deposit(amount)
        return True

