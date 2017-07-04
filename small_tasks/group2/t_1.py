'''
TODO add description
'''

def first_task():
    from itertools import chain, repeat

    def var1(keys, values):
        res = {}
        count = 0
        val_len = len(values)
        for k in keys:
            if count < val_len:
                v = values[count]
            else:
                v = None
            res.update({k: v})
            count += 1
        return res

    def var2(keys, values):
        return dict(zip(keys, chain(values, repeat(None))))

    test_set = (
        (range(10), range(5)),
        (range(5), range(10)),
        ([], []),
        ([1], [])
    )

    for k,v in test_set:
        print('KEYS: %s - VALS: %s'% (k, v))
        print(var1(k, v))
        print(var2(k, v))

