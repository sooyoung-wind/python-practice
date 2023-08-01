# -*- coding: utf-8 -*-
"""
Created on Tue Aug  1 15:42:56 2023

@author: 김동억
"""

import contextlib
from enum import auto, Enum

import pyttsx3
from abc import abstractmethod, ABCMeta


@contextlib.contextmanager
def tts_engine():
    engine = pyttsx3.init()
    engine.setProperty('rate', 240)
    yield engine  # __enter__
    engine.stop()  # __exit__


class NotEnoughMoneyError(Exception):
    pass

### enum으로 사용해서 before에 1, after에 2 입력
### user_input을 1, notify_message을 2로 
class SayOrder(Enum):
    BEFORE = auto(),
    AFTER = auto()

### enum으로 사용해서 FINISH 1, PROGRESS에 2 입력
### 숫자 1과 2를 사용해서 프로그램 종료 여부를 확인...
class TradingProgress(Enum):
    FINISH = auto(),
    PROGRESS = auto()


def say_message(order):
    def say(func):
        def wrapper(*args, **kwargs):
            if order is SayOrder.BEFORE:
                if args[1] is not None and type(args[1]) is str:
                    tts_say(args[1])

            ret = func(*args, **kwargs)
            if order is SayOrder.AFTER:
                if args[1] is not None and type(args[1]) is str:
                    tts_say(args[1])
            return ret

        def tts_say(msg):
            with tts_engine() as engine:
                engine.say(msg)
                engine.runAndWait()

        return wrapper

    return say


class BankAccount:
    def __init__(self, balance: int = 0):
        self.balance = balance

    def deposit(self, amount: int):
        self.balance += amount
        self.notify_deposit(amount)

    def withdraw(self, amount: int):
        if amount > self.balance:
            raise NotEnoughMoneyError()
        self.balance -= amount
        self.notify_withdraw(amount)

    def describe_balance(self):
        self.notify_message(self.create_balance_message())

    def create_balance_message(self):
        return f"잔액은 {self.balance}원 입니다."

    def notify_deposit(self, amount: int):
        self.notify_message(f"{amount}원을 입금했습니다. {self.create_balance_message()}")

    def notify_withdraw(self, amount: int):
        self.notify_message(f"{amount}원을 출금했습니다. {self.create_balance_message()}")

    @say_message(order=SayOrder.AFTER)
    def notify_message(self, message: str):
        print(message)


class ATMFunction(metaclass=ABCMeta):
    def __init__(self, account: BankAccount = None):
        self.account = account

    @say_message(order=SayOrder.BEFORE)
    def user_input(self, message):
        ret = int(input(message))
        return ret

    @say_message(order=SayOrder.AFTER)
    def notify_message(self, message):
        print(message)

    @abstractmethod
    def play(self) -> TradingProgress:
        pass


class Deposit(ATMFunction):
    def play(self):
        money = self.user_input('입금할 금액을 입력해 주세요.')
        self.account.deposit(money)
        return TradingProgress.PROGRESS


class Withdraw(ATMFunction):
    def play(self):
        money = self.user_input('출금할 금액을 입력해 주세요. : ')
        try:
            self.account.withdraw(money)
        except NotEnoughMoneyError:
            self.notify_message('출금할 금액이 잔고보다 큽니다. 다시 입력해 주세요.')
        return TradingProgress.PROGRESS


class Describe(ATMFunction):
    def play(self):
        self.account.describe_balance()
        return TradingProgress.PROGRESS


class Finish(ATMFunction):
    def play(self):
        self.notify_message('이용해 주셔서 감사합니다.')
        return TradingProgress.FINISH


class NotSupported(ATMFunction):
    def play(self):
        self.notify_message('지원하지 않는 메뉴 숫자입니다. 다시 입력해 주세요.')
        return TradingProgress.PROGRESS


class ATMFunctionStore:
    def __init__(self, account):
        self.deposit = Deposit(account)
        self.withdraw = Withdraw(account)
        self.describe = Describe(account)
        self.finish = Finish()
        self.not_supported = NotSupported()

    def get_function(self, num):
        if num == 1:
            return self.deposit
        elif num == 2:
            return self.withdraw
        elif num == 3:
            return self.describe
        elif num == 4:
            return self.finish
        else:
            return self.not_supported


class ATM:
    def __init__(self, account: BankAccount):
        self.function_store = ATMFunctionStore(account)

    def run(self):
        while True:
            try:
                self.print_menu()
                f = self.get_function()
                if f.play() is TradingProgress.FINISH:
                    break
            except ValueError:
                self.notify_message('숫자만 입력해 주세요. 처음부터 다시 시작합니다.')

    def get_function(self):
        self.notify_message('원하시는 서비스 메뉴를 숫자로 입력해 주세요.')
        menu_number = int(input('메뉴 선택 : '))
        return self.function_store.get_function(menu_number)

    def print_menu(self):
        msg = '''
    1. 입금
    2. 출금
    3. 잔액 확인
    4. 종료
            '''
        print('안녕하세요 AI 은행입니다.')
        print('----------------------')
        self.notify_message(msg)
        print('----------------------')

    @say_message(order=SayOrder.AFTER)
    def notify_message(self, message):
        print(message)


bank_account = BankAccount(1_000_000)
atm = ATM(bank_account)
atm.run()