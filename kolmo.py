# kolmogorov complexity of extremely finite strings

def f0():
    result = ""; length = 1
    while len(result) < length:
        result += "0"
    return result

def f1():
    result = ""; length = 1
    while len(result) < length:
        result += "1"
    return result

def f00():
    result = ""; length = 2
    while len(result) < length:
        result += "0"
    return result

def f11():
    result = ""; length = 2
    while len(result) < length:
        result += "1"
    return result

def f01():
    result = ""; length = 2
    while len(result) < length:
        if len(result) == 0:
            result += "0"
        else:
            result += "1"
    return result

def f10():
    result = ""; length = 2
    while len(result) < length:
        if len(result) == 0:
            result += "1"
        else:
            result += "0"
    return result

def f010():
    result = ""; length = 3
    state0 = 0
    while len(result) < length:
        result += str(state0)
        state0 = (state0 + 1) % 2
    return result

def f0010():
    result = ""; length = 4
    state0 = 0
    while len(result) < length:
        if len(result) == 0:
            result += "0"
        else:
            result += str(state0)
            state0 = (state0 + 1) % 2
    return result

def f01001():
    result = ""; length = 5
    state0 = 0
    while len(result) < length:
        if len(result) == 3:
            result += "0"
        else:
            result += str(state0)
            state0 = (state0 + 1) % 2
    return result

def f00101():
    result = ""; length = 5
    state0 = 0
    while len(result) < length:
        if len(result) == 1:
            result += "0"
        else:
            result += str(state0)
            state0 = (state0 + 1) % 2
    return result

def f011010():
    result = ""; length = 6
    state0 = 0
    while len(result) < length:
        if len(result) == 2:
            result += "1"
        else:
            result += str(state0)
            state0 = (state0 + 1) % 2
    return result

def f000110():
    result = ""; length = 6
    while len(result) < length:
        if len(result) < 2:
            result += "0"
        elif len(result) < 4:
            result += "1"
        else:
            result += "0"
    return result

def f000110_alt():
    result = ""; length = 6
    while len(result) < length:
        if len(result) < 2:
            result += "0"
        elif len(result) < 4:
            result += "1"
        else:
            result += "0"
    return result

print(f0()) # score: 1 (unless adding the while loop is a "cost")
print(f1()) # score: 1 (unless adding the while loop is a "cost")
print(f00()) # score: 1
print(f11()) # score: 1
print(f01()) # score: 2
print(f10()) # score: 2
print(f010()) # score: 2
print(f0010()) # score: 3   a
print(f01001()) # score: 3  a
print(f00101()) # score: 3  a
print(f011010()) # score: 3 a
print(f000110()) # score: 3 b *im not sure if a 1-bit state lets this one avoid 3 if-branches! arguably more complex

# postulates:
# 000 | 1
# 111 | 1
# 011 | 2
# 110 | 2
# 100 | 2
# 001 | 2
# 010 | 2-3 (2?)
# 101 | 2-3 (2?)
# 0000 | 1
# 1111 | 1
# 0111 | 2 a
# 1110 | 2 a
# 1000 | 2 a
# 0001 | 2 a
# 0011 | 2 b
# 1100 | 2 b
# 0101 | 2-3 (2?)
# 1010 | 2-3 (2?)
# 0100 | 3? a
# 0010 | 3? a
# 1011 | 3? a
# 0100 | 3? a
# 0110 | 3? b
# 1001 | 3? b
# with strings of length 4 it seems the highest complexity is 3 maybe
# so then for n = 5; will the max be 4? is it generally n-1? I doubt that. I'm not sure.

# don't see how you could do better than that for any length-2 string

# intuitive ranking of "complexity" of strings:
# 0 vs 1: tie
# 00 vs 11 vs 01 vs 10: tie? (tho if I *had* to pick, I'd maybe call 01 and 10 more "complex", but how exactly?)
# 000 and 111 are surely less complex than 010 and 101. What about 001, 011, 110, 100?
# 0000000000 vs 0111001010? the first must be objectively simpler in some objective sense of objective!

# think about how hard it'd be for a turing machine to implement!
# or that's too complex; but what about if these functions get to know, for free, the end-of-string point where they should stop?
