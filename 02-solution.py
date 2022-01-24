def solution(s):
    # make sure s is str
    if (not isinstance(s, str)):
        return None
    # make sure s is between 1-100 chars long
    if (len(s) > 100 or len(s) < 1):
        return None
    
    salutes = 0
    for i in range(len(s)):
        # each '>' count num '<' in front *2
        if (s[i] == '>'):
            for j in s[i:len(s)]:
                if (j == '<'):
                    salutes += 2
    return salutes