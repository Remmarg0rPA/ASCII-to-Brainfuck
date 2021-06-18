#!/usr/bin/python3
from math import sqrt

def ascii_to_bf(ascii_text):
    '''
    Converts the string to Brainfuck code
    '''
    ascii_vals = [ord(i) for i in ascii_text]
    diffs = [ascii_vals[0]]
    diffs.extend( [(num - ascii_vals[i-1]) for i, num in enumerate(ascii_vals[1:], start=1)] )

    code = ''
    ptr = 0
    for d, v in zip(diffs, ascii_vals):
        c, ptr= diff_to_bf(d, v, ptr)
        code += c + '.'
    return code


def diff_to_bf(diff, val, ptr):
    '''
    Returns a somewhat efficient brainfuck code for the difference
    '''

    if diff == 0:
        return ('>' if ptr == 0 else ''), 1

    #TODO: Check what is the most efficient when val and diff are small
    # More efficient when difference is larger than value
    if val < -diff and abs(diff) > 10:
        num_loops, change, extra = get_optimal_nums(val)
        if num_loops != 1:
            code = ('>' if ptr == 0 else '') + '[-]<' + num_to_bf(num_loops, '+') + '[>' + num_to_bf(change) + '<-]>' + num_to_bf(extra)
        else:
            code = ('>' if ptr == 0 else '') + '[-]' + '+'*abs(change + extra)
        return code, 1

    sign = '+' if diff > 0 else '-'
    num_loops, change, extra = get_optimal_nums(diff)
    if num_loops == 1:
        code = ('>' if ptr == 0 else '') +  sign*abs(change + extra)
        return code, 1
    else:
        code = ('<' if ptr == 1 else '') + num_to_bf(num_loops) + '[>' + num_to_bf(change) + '<-]>' + num_to_bf(extra)
        return code, 1


def get_optimal_nums(val):
    '''
    Calculates an almost optimal way to add or subtract a number in brainfuck by calculating
    how many loops there should be and how much needs to be changed in and after each loop.
    Returns (num loops, change in loop, change after loop)
    '''
    sign = 1 if val > 0 else -1
    abs_val = abs(val)
    sr = int(sqrt(abs_val))
    ''' # Calculates what is the closest to val when squared.
        # Ex. 45 gives sr=6, but 6^2 + 9 is less efficient than 7^2-4, therfore sr=7 is better '''
    if abs(sr**2 - abs_val) > abs((sr + 1)**2 - abs_val):
        sr += 1
    sum  = sr*2 + abs(abs_val - sr**2)
    ret = (sr, sign*sr, sign*(abs_val - sr**2))

    # Get factors of val and their sum
    factors = get_factors(val)
    sum_factors = abs(factors[0]) + abs(factors[1])

    # Returns the combo with the smallest sum
    # If factors[0] (num loops) is 1 we need no brackets and can also remove '>' and '<-' and therefore we subtract 5
    if (sum_factors <= sum) or (factors[0] == 1 and sum_factors-5 <= sum ):
        return (factors[0], factors[1], 0)
    else:
        return ret

def get_factors(num):
    '''
    Returns the factors with the smallest sum (the ones closest to the sqrt)
    '''
    sr = int(sqrt(abs(num)))
    for i in range(sr, 2, -1):
        if num % i == 0:
            return i, num//i
    return 1, num


def num_to_bf(num, sign=None):
    ''' Converts -3 to '---', 4 to '++++', etc if sign is not given '''
    if sign is None:
        sign = '-' if num < 0 else '+'
    return sign * abs(num)


if __name__ == '__main__':
    ascii_str = 'Hello world!\n'
    o = ascii_to_bf(ascii_str)
    print(f"Length: {len(o)} \nCode:\n{o}")
