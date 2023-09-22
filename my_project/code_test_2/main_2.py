"""
Created on Fri Sep 22 10:31:25 2023

@author: Soo.Y
"""

import pytest
from hash_level2 import solution


def test_case_1():
    phone_book1 = ["119", "97674223", "1195524421"]
    assert solution(phone_book1) == False


def test_case_2():
    phone_book2 = ["123", "456", "789"]
    assert solution(phone_book2) == True


def test_case_3():
    phone_book3 = ["12", "123", "1235", "567", "88"]
    assert solution(phone_book3) == False


def test_case_4():
    phone_book4 = ["911", "97674223", "1195524421"]
    assert solution(phone_book4) == True


def test_case_5():
    phone_book7 = ["1", "2", "3", "4", "5"]
    assert solution(phone_book7) == True


def test_case_6():
    phone_book8 = ["12345678901234567890",
                   "23456789012345678901", "34567890123456789012"]
    assert solution(phone_book8) == True


def test_case_7():
    phone_book9 = ["1", "11", "2", "22", "111"]
    assert solution(phone_book9) == False


if __name__ == "__main__":
    pytest.main()
