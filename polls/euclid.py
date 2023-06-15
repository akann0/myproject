import time
def remainder(x, y):
    times = 0
    mainder = x
    while (mainder >= y):
        times += 1
        mainder -= y
    return [times, mainder]

def div_degree(x):
    degree = 0
    while (x[degree] == 0):
        degree += 1
    return len(x) - degree

def multiply(divby, y, length = 0):
    product = []
    #multiply everything in y by the constant in divby
    for i in range(len(y)):
        product.append(divby[0] * y[i])
    #add the degree of the divisor to the degree of the dividend
    for i in range(divby[1]):
        product.append(0)
    for i in range(length - len(product)):
        product.insert(0,0)
    return product

def multiply_two_polynomials(x, y, field):
    product = []
    for i in range(len(x) + len(y) - 1):
        product.append(0)
    for i in range(len(x)):
        for j in range(len(y)):
            product[i + j] += x[i] * y[j]
            if field != 'none':
                product[i + j] %= field
    return product



def subtract(x, y, field):
    difference = []
    for i in range(len(x)):
        difference.append(x[i])
    if  len(x) < len(y):
        for i in range(len(y) - len(x)):
            difference.insert(0,0)
    for i in range(len(y)):
        difference[i] -= y[i]
        #print(difference[i])
        if field != 'none':
            difference[i] %= field
    return difference

def inverse_of(x, y, field):
    if field == 'none':
        return x/y
    for i in range(field):
        if (y * i) % field == x:
            #print(i)
            return i
    return 0

def print_as_polynomial(x):
    stri = "$"
    for i in range(len(x)):
        if x[i] != 0 and x[i] != 1:
            if len(x) - i - 1 != 0 and len(x) - i - 1 != 1:
                stri += str(x[i]) + "x^" + str(len(x) - i - 1) + " + "
            elif len(x) - i - 1 == 1:
                stri += str(x[i]) + "x" + " + "
            else:
                stri += str(x[i]) + " + "
        elif x[i] == 1:
            if len(x) - i - 1 != 0 and len(x) - i - 1 != 1:
                stri += "x^" + str(len(x) - i - 1) + " + "
            elif len(x) - i - 1 == 1:
                stri += "x" + " + "
            else:
                stri += "1 + "
    stri = stri[:-3] + "$"
    print(stri)

def return_as_polynomial(x):
    stri = "$"
    for i in range(len(x)):
        if x[i] % 1 != 0:
            x[i] = round(x[i], 3)
        if x[i] != 0 and x[i] != 1:
            if len(x) - i - 1 != 0 and len(x) - i - 1 != 1:
                stri += str(x[i]) + "x^" + str(len(x) - i - 1) + " + "
            elif len(x) - i - 1 == 1:
                stri += str(x[i]) + "x" + " + "
            else:
                stri += str(x[i]) + " + "
        elif x[i] == 1:
            if len(x) - i - 1 != 0 and len(x) - i - 1 != 1:
                stri += "x^" + str(len(x) - i - 1) + " + "
            elif len(x) - i - 1 == 1:
                stri += "x" + " + "
            else:
                stri += "1 + "
    stri = stri[:-3] + "$"
    return stri

def division_algorithm(x, y, field, printout = True):
    #set quotient to an array of zeroes of length len(x) - len(y
    #print("$")
    if printout:
        print_as_polynomial(x)
        print("divided by")
        print_as_polynomial(y)
        if field != 'none':
            print("in $Z_" + str(field) + "[x]$")
    quotient = []
    for i in range(len(x)):
        quotient.append(0)
    divisor = y
    dividend = x
    dividend_degree = len(x) - 1
    while (dividend_degree >= len(divisor) - 1):
        divide_by = [inverse_of(dividend[len(x) - 1 - dividend_degree], divisor[0], field), dividend_degree - len(divisor) + 1]
        quotient[len(x) - divide_by[1] - 1] = divide_by[0]
        dividend = subtract(dividend, multiply(divide_by, y, len(x)), field)
        dividend_degree -= 1
    if printout:
        print("has a quotient of ")
        print_as_polynomial(quotient)
        print("and a remainder of ")
        print_as_polynomial(dividend)
    return [quotient, dividend]

print(division_algorithm([1, 0, 1, 1], [1, 0, 0], 2))


def notzero(x):
    for i in range(len(x)):
        if x[i] != 0:
            return True
    return False

def cutoutextrazeroes(x):
    for i in range(len(x)):
        if x[i] != 0:
            return x[i:]
    return [0]


def euclid(x, y, field='none'):
    chain = [x]
    while (notzero(y)):
        mainder = division_algorithm(x, y, field, False)
        chain.append(y)

        print(return_as_polynomial(x) + " = (" + return_as_polynomial(mainder[0]) + ")(" + return_as_polynomial(y) + ") + " + return_as_polynomial(mainder[1]))
        print()
        time.sleep(0.1)
        x = y
        y = cutoutextrazeroes(mainder[1])


    print("And the reverse:")
    print()
    chain.reverse()
    print(chain)
    print()
    x = [1]
    y = [1]


    for i in range(len(chain)):
        if i < 1:
            #print(str(chain[0]) + " = " + str(chain[0]) + " + 0")
            continue

        mainder = division_algorithm(chain[i], chain[i-1], field, False)

        #print(return_as_polynomial(chain[0]) + " = (" + return_as_polynomial(x) + ")(" + return_as_polynomial(chain[i-1]) + ") + (" + return_as_polynomial(y) + ")(" + return_as_polynomial(chain[i]) + ") - (" + return_as_polynomial(mainder[0]) + ")(" + return_as_polynomial(chain[i-1]) + ")")
        #print()
        xx = x
        x = y
        y = subtract(xx, multiply_two_polynomials(y, mainder[0], field), field)

        print(return_as_polynomial(chain[0]) + " = (" + return_as_polynomial(x) + ")(" + return_as_polynomial(chain[i]) + ") + ("  + return_as_polynomial(y) + ")(" + return_as_polynomial(chain[i-1]) + ")")
        print()





euclid([1, -6, 14, -15], [1, -8, 21, -18])
euclid([1, 1, -4, 4], [1, 0, 3, -2], 5)
euclid([1, 0, -2, 4], [4, 0, 1, 3])


cayley_table = []
cayley_table.append([0, 1, 2, 3])
cayley_table.append([1, 0, 2, 3])
cayley_table.append([2, 1, 0, 3])
cayley_table.append([3, 3, 1, 2])

def cayley():
    for a in range(3):
        for b in range(3):
            for c in range(3):
                first = cayley_table[cayley_table[a][b]][c]
                second = cayley_table[a][cayley_table[b][c]]

                if first != second:
                    print(str(a) + str(b) + str(c))

stri = ""
for i in range(12):
    stri = str(i)
    for j in range(12):
        stri += " & " + str((i * j) % 12)
    #print(stri)
    #print("\hline")
#print(stri)