# -*- coding: utf-8 -*-
"""
Created on Tue Sep 12 15:37:44 2023

@author: Soo.Y
"""

from collections import deque


def bfs(graph, start_point):
    my_memory_q = deque()
    my_memory_q.append(start_point)
    check_visited_dict = {start_point: True}

    while my_memory_q:
        search_point = my_memory_q.popleft()
        for next_point in graph[search_point]:
            if next_point not in check_visited_dict:
                my_memory_q.append(next_point)
                check_visited_dict[next_point] = True

    # print(check_visited_dict.keys())


check_visited_dict = {}


def dfs(graph, start_point):
    check_visited_dict[start_point] = True
    for next_point in graph[start_point]:
        if next_point not in check_visited_dict:
            dfs(graph, next_point)

# print(check_visited_dict.keys())


graph = {
    0: [1, 3, 6],
    1: [0, 3],
    2: [3],
    3: [0, 1, 2, 7],
    4: [5],
    5: [4, 6, 7],
    6: [0, 5],
    7: [3, 5],
}

bfs(graph, start_point=0)
dfs(graph, start_point=0)
# print(check_visited_dict.keys())

q1 = deque()
visited = {}


def bfs(graph, start_v):  # 재귀
    visited[start_v] = True
    print(start_v)
    for node in graph[start_v]:
        if node not in visited:
            visited[node] = True
            q1.append(node)
    if q1:
        bfs(graph, q1.popleft())


bfs(graph, start_v=0)
