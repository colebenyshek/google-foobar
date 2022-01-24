def solution(M, F):
    big = max(int(M), int(F))
    small = min(int(M), int(F))
    regens = 0
    while small > 0:
        regens = regens + (big//small)
        temp = big
        big = small
        small = temp % big
    if (big != 1):
        return 'impossible'
    return (str(regens-1))