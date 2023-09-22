"""
Created on Fri Sep 22 10:10:45 2023

@author: Soo.Y
"""

import pytest
from hash_level1 import solution


def test_solution():
    assert solution(["leo", "kiki", "eden"], ["eden", "kiki"]) == "leo"
    assert solution(["marina", "josipa", "nikola", "vinko", "filipa"], [
                    "josipa", "filipa", "marina", "nikola"]) == "vinko"
    assert solution(["mislav", "stanko", "mislav", "ana"], [
                    "stanko", "ana", "mislav"]) == "mislav"
    assert solution(["a", "b", "c"], ["a", "b"]) == "c"
    assert solution(["x", "y", "z", "z"], ["x", "z", "z"]) == "y"
    assert solution(["apple", "banana", "cherry"], [
                    "apple", "banana"]) == "cherry"
    assert solution(["one", "two", "three", "two"], [
                    "one", "two", "three"]) == "two"
    assert solution(["a"], []) == "a"


def test_duplicate_case():
    assert solution(["a", "a", "b", "c"], ["a", "c", "b"]) == "a"
    assert solution(["x", "y", "z", "z"], ["x", "z", "z", "x"]) == "y"
    assert solution(["apple", "banana", "cherry", "cherry"], [
                    "apple", "banana", "cherry"]) == "cherry"
    assert solution(["one", "two", "two", "two"], [
                    "one", "two", "two"]) == "two"
    assert solution(["a", "a", "a"], ["a", "a"]) == "a"


def test_large_size_case():
    large_participant = ["participant" + str(i) for i in range(1, 100001)]
    large_completion = ["participant" + str(i) for i in range(1, 100000)]
    assert solution(large_participant, large_completion) == "participant100000"


if __name__ == "__main__":
    pytest.main()
