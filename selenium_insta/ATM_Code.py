# -*- coding: utf-8 -*-
"""
Created on Mon Jul 31 15:26:49 2023

@author: Soo.Y
"""
# 연습문제 

import pyttsx3

class Account:
    def __init__(self, balance):
        self.balance = balance
    
    def card_or_bank(self):
        msg = '''
        ============================
        1. 카드
        2. 무통장
        ============================
        '''
        print(msg)
        
        engine = pyttsx3.init()
        engine.say('카드 및 무통장을 선택해주세요. : ')
        engine.runAndWait()
        value = int(input('카드 및 무통장을 선택해주세요. : '))
                
        if value == 1:
            self.deposit()
        elif value == 2:
            self.deposit()
        else:
            print("입력이 잘못되었습니다.")
            engine = pyttsx3.init()
            engine.say("입력이 잘못되었습니다.")
            engine.runAndWait()
    
    def deposit(self):
        
        engine = pyttsx3.init()
        engine.say('입금할 금액을 입력해주세요.')
        engine.runAndWait()
        deposit_value = int(input('입금할 금액을 입력해주세요. :'))

        self.balance += deposit_value
        print(f'{deposit_value}원 입금하셨고 잔액은 {self.balance}원 입니다.')
    
    def withdraw(self):
        engine = pyttsx3.init()
        engine.say('출금할 금액을 입력해주세요.')
        engine.runAndWait()
        withdraw_value = int(input('출금할 금액을 입력해주세요. :'))
        if self.balance >= withdraw_value:
            self.balance -= withdraw_value
            print(f'{withdraw_value}원 출금하셨고 잔액은 {self.balance}원 입니다.')
        else:
            engine = pyttsx3.init()
            engine.say('잔액이 부족합니다.')
            engine.runAndWait()
            print('잔액이 부족합니다.')
    
    def check_balance(self):
        print(f'현재 잔액은 {self.balance}입니다.')
        
Soo_account = Account(30000)

while True:
    msg = '''
    안녕하세요. AI 은행입니다. 원하시는 서비스 번호를 입력해주세요.
    1. 입금
    2. 출금
    3. 잔액확인
    4. 종료
    '''
    print(msg)
    engine = pyttsx3.init()
    engine.say('안녕하세요. AI 은행입니다. 원하시는 서비스 번호를 입력해주세요.')
    engine.runAndWait()
    
    
    menu = int(input('원하시는 서비스 번호를 입력해주세요. :'))

    if menu == 1:
        Soo_account.card_or_bank()
    elif menu == 2:
        Soo_account.withdraw()
    elif menu == 3:
        Soo_account.check_balance()
    elif menu == 4:
        print('이용해 주셔서 감사합니다.')
        break
    else:
        print('번호를 잘못 입력하셨습니다.')
    
    

