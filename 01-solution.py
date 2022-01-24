def solution(x):
    # string to list -> chars to unicode -> invert unicode for a...z --> revert to chars --> join
    message = list(x)
    for i in range(len(message)):
        message[i] = ord(message[i])
        if (message[i] >= 97 and message[i] <= 122):
            message[i] = (122+97) - message[i]
        message[i] = chr(message[i])
    return ''.join(message)
