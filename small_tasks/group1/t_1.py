'''
There is a list of 1000 elements.
* Get only values
* Get reversed version of the list

'''

t = range(1000)

odd_list = [v for v in t if v % 2 != 0]

reversed_list = t[::-1] # honestly it's a range :)
