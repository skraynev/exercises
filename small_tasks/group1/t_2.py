'''
Write decorator for counting calls of the function
'''


def count_call(func):
    def wrapper(*args, **kwargs):
        ''' Add "count" attribute for wrapper '''
        func(*args, **kwargs)
        wrapper.count += 1
        print("Function called %s times" % wrapper.count)
    wrapper.count = 0
    return wrapper


@count_call
def test():
    print('test')


if __name__ == '__main__':
    test()
    test()
    test()
    test()
