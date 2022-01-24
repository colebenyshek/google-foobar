def solution(n):
    # Use memo to reduce time (slow for large N)
    memo = [[0 for i in range(n+2)] for j in range(n+2)]

    # helper function for all stairs of size n
    # -1 used since a single stair of height n is not acceptable
    return helper(1,n,memo) - 1

def helper(height, remaining, array):
    # if solution already exists, return
    if (array[height][remaining] != 0):
        return array[height][remaining]
    # all the bricks are used (a solution!)
    if (remaining == 0):
        return 1
    # not enough bricks to build stair at this height
    if (remaining < height):
        return 0
    
    # use stair resource and move on
    # or try next stair height
    newStair = helper(height + 1, remaining - height, array)
    newHeight = helper(height + 1, remaining, array)

    # store value
    array[height][remaining] = newStair + newHeight
    for i in range(len(array)):
        print(array[i])
    print('-------------')
    return newStair + newHeight
