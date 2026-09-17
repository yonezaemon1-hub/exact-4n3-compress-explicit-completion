#!/usr/bin/env python3
"""Model and exact helpers for the explicit completion studied in Paper 14.

Standard-library only. This module contains the transition system, witness/reset
constructions, and exact pair-automaton routines shared by the public experiment
and proof-audit scripts.
"""
from collections import defaultdict, deque


def automaton(k):
    if k < 1:
        raise ValueError("k must be >= 1")
    n = 3 * k + 6
    A, B, M = 2 * k + 4, 2 * k + 5, 3 * k + 5
    a = [None] * n
    b = [None] * n
    for i in range(n):
        if i == 0:
            a[i] = 0
        elif 1 <= i <= 2 * k + 3 and i % 2 == 1:
            a[i] = i + 1
        elif 1 <= i <= 2 * k + 3 and i % 2 == 0:
            a[i] = i - 1
        elif A <= i < M and i % 2 == 0:
            a[i] = i + 1
        elif 2 * k + 7 <= i < M and i % 2 == 1:
            a[i] = i - 1
        elif i == B:
            a[i] = 3
        elif i == M and i % 2 == 0:
            a[i] = M
        elif i == M and i % 2 == 1:
            a[i] = M - 1

        if i == 0:
            b[i] = 1
        elif 1 <= i <= 2 * k + 3 and i % 2 == 0:
            b[i] = i + 1
        elif 1 <= i <= 2 * k + 3 and i % 2 == 1:
            b[i] = i - 1
        elif B <= i < M and i % 2 == 1:
            b[i] = i + 1
        elif 2 * k + 6 <= i < M and i % 2 == 0:
            b[i] = i - 1
        elif i == A:
            b[i] = 2
        elif i == M and i % 2 == 1:
            b[i] = M
        elif i == M and i % 2 == 0:
            b[i] = M - 1

    if any(x is None for x in a) or any(x is None for x in b):
        raise AssertionError("transition function is not total")
    return a, b


def image_state(q, word, a, b):
    for ch in word:
        q = a[q] if ch == "a" else b[q]
    return q


def image_set(states, word, a, b):
    s = set(states)
    for ch in word:
        arr = a if ch == "a" else b
        s = {arr[q] for q in s}
    return s


def c_word(k):
    return "ba" * (k + 2) + "ab" * (k + 2)


def B_word(r):
    if r < 1 or r % 2 != 1:
        raise ValueError("r must be a positive odd integer")
    return "ba" * ((r - 1) // 2) + "b"


def reset_word(k):
    parts = [B_word(2 * k + 3), "aa", B_word(2 * k + 1), "aaaa", B_word(2 * k - 1)]
    for j in range(k + 1):
        parts.extend(["aa", B_word(4 * k + 3 - 2 * j)])
    parts.extend(["aa", B_word(2 * k + 3)])
    return "".join(parts)


def letter_profile(arr):
    inv = defaultdict(list)
    for i, x in enumerate(arr):
        inv[x].append(i)
    collisions = [tuple(v) for v in inv.values() if len(v) > 1]
    missing = sorted(set(range(len(arr))) - set(arr))
    return len(set(arr)), collisions, missing


def pair_distances_to_diagonal(k):
    """Exact shortest merge distance for every unordered pair."""
    a, b = automaton(k)
    n = len(a)
    rev = defaultdict(list)
    for i in range(n):
        for j in range(i, n):
            for arr in (a, b):
                x, y = arr[i], arr[j]
                if x > y:
                    x, y = y, x
                rev[(x, y)].append((i, j))
    d = {}
    q = deque()
    for i in range(n):
        d[(i, i)] = 0
        q.append((i, i))
    while q:
        y = q.popleft()
        for x in rev[y]:
            if x not in d:
                d[x] = d[y] + 1
                q.append(x)
    return d


def q0_threshold(k):
    d = pair_distances_to_diagonal(k)
    n = 3 * k + 6
    threshold = min(d[(0, j)] for j in range(1, n))
    minimizers = [j for j in range(1, n) if d[(0, j)] == threshold]
    return threshold, minimizers


def reverse_layers_from_collision_pairs(k, max_depth):
    """Reverse BFS in the non-diagonal pair graph from the two final collisions."""
    a, b = automaton(k)
    n = len(a)
    A, B = 2 * k + 4, 2 * k + 5
    targets = {(3, A), (4, B)}
    rev = defaultdict(set)
    for i in range(n):
        for j in range(i + 1, n):
            for arr in (a, b):
                x, y = arr[i], arr[j]
                if x == y:
                    continue
                if x > y:
                    x, y = y, x
                rev[(x, y)].add((i, j))
    dist = {p: 0 for p in targets}
    q = deque(targets)
    while q:
        y = q.popleft()
        if dist[y] >= max_depth:
            continue
        for x in rev[y]:
            if x not in dist:
                dist[x] = dist[y] + 1
                q.append(x)
    layers = defaultdict(set)
    for p, depth in dist.items():
        layers[depth].add(p)
    return layers


def template_layers(k):
    """Closed-form reverse frontier used by the manuscript for k >= 5."""
    A, B, M = 2 * k + 4, 2 * k + 5, 3 * k + 5
    T = defaultdict(set)

    for t in range(k + 1):
        T[t].add(tuple(sorted((3 + t, A - t))))
        T[t].add(tuple(sorted((4 + t, B + t))))
        if t >= 1:
            T[t].add(tuple(sorted((A - t, A + t))))

    for s in range(1, k + 2):
        t = k + s
        F = (k + 3, M) if s == 1 else (k + 4 - s, M - s + 2)
        T[t].add(tuple(sorted(F)))
        if s <= k - 1:
            T[t].add(tuple(sorted((k + 4 + s, M - s + 1))))

    for r in range(k + 3):
        t = 2 * k + 2 + r
        H = (2, B) if r == 0 else (r, A + 1 - r)
        T[t].add(tuple(sorted(H)))
        if r == 1:
            T[t].add((A, A + 2))
        elif r >= 3:
            T[t].add(tuple(sorted((A + 1 - r, A + 3 - r))))
        if r >= 4:
            T[t].add(tuple(sorted((A + 1 - r, A + r - 3))))
        if r <= k - 2:
            T[t].add((A + 1 + r, A + 3 + r))
        if r == k - 1:
            T[t].add((M - 1, M))

    for s in range(k + 2):
        t = 3 * k + 5 + s
        T[t].add(tuple(sorted((k + 2 - s, k + 4 - s))))
        if s == 0:
            V = (k + 2, M - 1)
        elif s == 1:
            V = (k + 1, M)
        else:
            V = (k + 2 - s, M - s + 2)
        T[t].add(tuple(sorted(V)))
        if s == k:
            T[t].add((6, B))
            T[t].add((B, B + 4))
        if s == k + 1:
            for p in ((5, A), (7, A + 2), (A, A + 4), (A + 2, A + 6)):
                T[t].add(tuple(sorted(p)))
    return T
