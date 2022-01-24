from fractions import Fraction
import copy
import fractions

def solution(m):

    # check if case where s0 is terminal state
    count = 0
    for i in range(len(m[0])):
        count += m[0][i]
    if (not count):
        end = [1]
        for i in range(1,len(m)):
            t = 0
            for j in range(len(m[i])):
                t += m[i][j]
            if (not t):
                end.append(0)
        end.append(1)
        return end

    p = pMatrix(m)
    key = getKey(p)
    q = getQ(p)
    r = getR(p)
    n = getN(q)
    nr = getNR(n,r)
    L = getL(nr, p)

    index = key.index(0)
    zeroState = []
    lcd = 0
    for j in range(len(nr[0])):
        zeroState.append(L[index][(len(L)-len(nr[0])+j)])
        zeroState[j] = Fraction(zeroState[j])
        if (not j):
            lcd = zeroState[j].denominator
        else:
            lcd = lcm(zeroState[j].denominator, lcd)

    answer = []
    for i in range(len(zeroState)):
        answer.append(int(zeroState[i].numerator * (lcd // zeroState[i].denominator)))
    answer.append(lcd)
    return answer

# create probability matrix p
# (note: this also sorts matrix into canonical form)
def pMatrix(a):
    rows = len(a)
    cols = len(a[0])
    p = [[0 for x in range(cols)] for x in range(rows)]
    key = []
    count = 0
    for i in range(rows):
        count = sum(a[i])
        for j in range(cols):
            if (a[i][j] != 0):
                p[i][j] = Fraction(a[i][j], count)
        if (not count):
            p[i][i] = 1
            key.append(i)
        count = 0
    
    for i in range(rows-1, -1, -1):
        if(not i in key):
            key.insert(0, i)

    # put in canonical form
    p = organizeP(p, key)
    p.append(key)
    return p

# sort probability matrix (p) into canonical form
#      [Q, R]
#      [0, I]
def organizeP(pMatrix, order):
    temp = copy.deepcopy(pMatrix)
    for i, x in zip(order, range(len(pMatrix))):
        for j, y in zip(order, range(len(pMatrix[x]))):
            pMatrix[x][y] = temp[i][j]
    return pMatrix

# remove order key from matrix p and return
def getKey(p):
    key = p.pop(len(p)-1)
    return key

# returns Q matrix of canonical P matrix
def getQ(p):
    index = getIdentityIndex(p)
    q = [[0 for x in range(index)] for x in range(index)]
    for i in range(len(q)):
        for j in range(len(q[i])):
            q[i][j] = p[i][j]
    return q

# returns R matrix of canonical P matrix
def getR(p):
    index = getIdentityIndex(p)
    r = [[0 for x in range(len(p)-index)] for x in range(index)]
    for i in range(len(r)):
        for j in range(index, len(r[i])+index):
            r[i][j-index] = p[i][j]
    return r

# returns I matrix of canonical P matrix
def getI(p):
    index = getIdentityIndex(p)
    id = [[0 for x in range(len(p)-index)] for x in range(len(p)-index)]
    for i in range(len(id)):
        id[i][i] = 1
    return id

# returns fundamental matrix (N) of canonical P matrix
# N = (I-Q)^-1
def getN(q):
    iq = [[0 for x in range(len(q))] for x in range(len(q))]
    for i in range(len(q)):
        for j in range(len(q[i])):
            if (i == j):
                iq[i][j] = 1 - q[i][j]
            else:
                iq[i][j] = (-1) * q[i][j]
    n = getInverse(iq)
    return n

# multiplies N & R matrices
def getNR(n, r):
    result = [[0 for i in range(len(r[0]))] for j in range(len(n))]
    # iterate through rows of n
    for i in range(len(n)):
        # iterate through columns of r
        for j in range(len(r[0])):
            # iterate through rows of r
            for k in range(len(r)):
                result[i][j] += n[i][k] * r[k][j]
    return result

def getL(nr, p):
    L = copy.deepcopy(p)
    for i in range(len(L)):
        for j in range(len(L[i])):
            if (j <= len(L)-len(nr[0])-1):
                L[i][j] = 0
            elif (i <= len(nr)-1):
                L[i][j] = nr[i][j-len(nr)]
            else:
                if (i == j):
                    L[i][j] = 1
    return L

# returns A^-1 where A is matrix
def getInverse(m):
    if (len(m) == 1):
        return [[m[0][0]**(-1)]]
    det = getDeterminant(m)
    adj = getAdjoint(m)
    inv = [[0 for i in range(len(m))] for j in range(len(m))]
    for i in range(len(m)):
        for j in range(len(m[i])):
            inv[i][j] = Fraction(adj[i][j], det)
    return inv

# find adjoint matrix
def getAdjoint(m):
    # create cofactor matrix
    cofactor = [[0 for i in range(len(m))] for j in range(len(m))]
    for i in range(len(m)):
        for j in range(len(m[i])):
            cofactor[i][j] = getDeterminant(getCofactor(m, i, j)) * ((-1) ** (i+j))
    adj = transpose(cofactor)
    return adj

 
# find minor cofactor matrix with row i col j 
def getCofactor(m, i, j):
    if (len(m) == 1):
        return m
    else:
        return [row[: j] + row[j+1:] for row in (m[: i] + m[i+1:])]
 


# find matrix determinant 
def getDeterminant(m):
    if (len(m) == 1):
        return m[0][0]
    # det for 2x2 matrix (recusion limit)
    if(len(m) == 2):
        value = m[0][0] * m[1][1] - m[1][0] * m[0][1]
        return value
    result = 0
    # for each column
    # find cofactor --> find det of that cofactor
    for current_column in range(len(m)):
        # change sign each term based on Lebniz formula
        sign = (-1) ** (current_column)
        sub_det = getDeterminant(getCofactor(m, 0, current_column))
        result += (sign * m[0][current_column] * sub_det)
    return result
 
# transpose a matrix m
def transpose(m):
    return [[m[j][i] for j in range(len(m))] for i in range(len(m[0]))]

# find index of top-left corner of identity matrix
# matrix is assumed to be organized p matrix
def getIdentityIndex(matrix):
    index = 0
    for i in range(len(matrix)):
        for j in range(len(matrix[i])):
            if (matrix[i][j] == 1 and isinstance(matrix[i][j], int)):
                index = i
                break
        if (index):
            break
    return index

# find greatest common divisor
def gcd(x, y):
    while(y):
        x,y = y, x%y
    return x

# find the least common multiple
def lcm(x, y):
    return int(abs(x * y) / gcd(x, y))

