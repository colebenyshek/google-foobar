
def solution(l):
    # check that l is a list
    if (not isinstance(l, list)):
        return None
    
    # check that l is 1-100 items long
    if (len(l) > 100 or len(l) < 1):
        return None

    # split strings into chars w/o '.'
    # cast chars into ints (to avoid sorting errors)
    for i in range(len(l)):
        l[i] = l[i].split('.')
        l[i] = list(map(lambda s: int(s), l[i]))

    # sort 
    l.sort()

    # cast ints back to chars and rejoin into strings
    for k in range(len(l)):
        l[k] = list(map(lambda s: str(s), l[k]))
        l[k] = '.'.join(l[k])

    return l
