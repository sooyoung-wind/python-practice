"""
Created on Fri Sep 22 10:31:50 2023

@author: Soo.Y
"""

# 단순 코테를 위한 풀이...문제가 제일 첫번째만 target으로 바라보고 있어서.....^^


def solution(phone_book):
    from collections import deque
    phone_book = deque(phone_book)
    target_number = phone_book.popleft()
    length_number = len(target_number)
    for phone_number in phone_book:
        if target_number == phone_number[0:length_number]:
            return False
    return True
