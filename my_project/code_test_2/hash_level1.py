"""
Created on Fri Sep 22 10:11:45 2023

@author: Soo.Y
"""


def solution(participant, completion):
    for completion_name in completion:
        if completion_name in participant:
            participant.remove(completion_name)

    return participant.pop()
