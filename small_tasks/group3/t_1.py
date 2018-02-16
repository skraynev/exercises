'''
Find all combinations of operands (+-*/) in left part of the string
1234567890 = 100, which make this equality correct
'''

from itertools import product
from itertools import zip_longest
import operator
from time import time


vals = (1, 2, 3, 4, 5, 6, 7, 8, 9, 0)


def _check_input_vals(vals):
    # skip one value and empty:
    if not vals:
        raise ValueError('Empty input "vals" list')
    elif len(vals) == 1:
        raise ValueError('"vals" list contains only one value')
    # some other optional check for vals .... (which you may imagine :) )
    pass

def _check_devision_on_zero(vals, ops):
    # skip combination where last operation is division on zero
    for i, op in enumerate(ops):
        if op is operator.truediv and vals[i + 1] == 0:
            return True
    return False


def safe_way(vals):
    ''' Calculate math in string manually with check of priority '''
    _check_input_vals(vals)

    counter = 0
    ops_tuple = (operator.add, operator.sub, operator.mul, operator.truediv)
    priority_ops = ops_tuple[2:]

    # help method for calculating one of two operations based on priority
    def calc(op1, op2, val1, val2, val3):
        if op1 in priority_ops or op2 not in priority_ops:
            return op1(val1, val2), val3, op2
        else:
            return val1, op2(val2, val3), op1

    for ops in product(ops_tuple, repeat=len(vals)-1):
        if _check_devision_on_zero(vals, ops):
            continue

        t_ops = list(ops)
        t_vals = list(vals)

        res = None
        while t_ops:
            if len(t_ops) > 1:
                op1, op2 = t_ops.pop(0), t_ops.pop(0)
                v1, v2, v3 = t_vals.pop(0), t_vals.pop(0), t_vals.pop(0)
                v1_, v2_, op_ = calc(op1, op2, v1, v2, v3)
                t_ops = [op_] + t_ops
                t_vals = [v1_, v2_] + t_vals
            else:
                op = t_ops.pop(0)
                res = op(t_vals.pop(0), t_vals.pop(0))

        if res == 100:
            counter += 1

    return counter


def fast_way(vals):
    ''' Use eval for calculation math in string '''
    _check_input_vals(vals)

    counter = 0
    ops_vals = '+-*/'
    for ops in product(ops_vals, repeat=len(vals) - 1):
        calc_str = ''
        for val, op in zip_longest(vals, ops, fillvalue=''):
            calc_str += str(val) + str(op)

        try:
            res = eval(calc_str)
        except ZeroDivisionError:
            # skip case, when it tries to divide on zero
            continue

        if res == 100:
            #print(res, ops)
            counter += 1
    return counter

ts = time()
print('Fast res: ', fast_way(vals), 'Time: ', time() - ts)
# btw Safe is also works faster
ts = time()
print('Safe res: ', safe_way(vals), 'Time: ', time() - ts)
