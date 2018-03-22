import ipaddress
from typing import Optional

test_data = [
    {
        # Example 1
        'in': ['10.0.0.0/24', '10.0.1.0/24'],
        'out': '10.0.0.0/23'
    },
    {
        # Example 2
        'in': ['10.0.1.0/24', '10.0.2.0/24'],
        'out': '10.0.0.0/22'
    },
    {
        # Example 3
        'in': ['10.0.0.0/23', '10.0.1.0/24'],
        'out': '10.0.0.0/23'
    },
    {
        # Example 4
        'in': ['10.0.0.0/8', '9.0.0.0/8'],
        'out': '8.0.0.0/6'
    },
    {
        # Example 5
        'in': ['10.0.0.0/8', '9.0.0.0/8', '5.0.0.0/8'],
        'out': '0.0.0.0/4'
    },
    # Extras
    {
        # []
        'in': [],
        'out': None
    },
    {
        # None
        'in': None,
        'out': None
    },
    {
        # one value
        'in': ['10.0.0.0/8'],
        'out': '10.0.0.0/8'
    },
    {
        # already equals
        'in': ['10.0.1.0/24', '10.0.1.0/24', '10.0.1.0/24'],
        'out': '10.0.1.0/24'
    },
    {
        # first two have lower subnet, but it's not the same as last one
        'in': ['10.0.1.0/24', '10.0.2.0/24', '10.0.0.0/12'],
        'out': '10.0.0.0/12'
    },
    {
        # no matches
        'in': ['10.0.0.0/8', '192.0.0.0/2'],
        'out': None
    },
]


# new_prefix
def find_common_subnet(subnets: Optional[list]) -> Optional[str]:
    # Assume, that all elements in the list are correct
    # Otherwise implement validation
    pass

    if not subnets:
        # Need to process situation, when input is empty
        # It was not mentioned in task, so return None
        return None

    if len(subnets) == 1:
        # if there is only one element, that it a answer
        return subnets[0]

    # Main logic
    # Parse subnets with ipaddress lib
    parsed = {ipaddress.ip_network(sub) for sub in subnets}
    # Get minimal prefixlen
    min_pref = min(p.prefixlen for p in parsed)

    # Algorigth:
    # 0. find minimal prefix and used it in step 1
    # 1. apply prefix for all supernets
    # 2. squash equals
    # 3. descrese prefix and repeat from step 1
    #    (if elements > 1 and min_pref > 0)
    while len(parsed) != 1 and min_pref > 0:
        parsed = {p.supernet(new_prefix=min_pref) for p in parsed}
        min_pref -= 1

    if len(parsed) != 1:
        # can not find common network
        return None

    return parsed.pop().exploded


# prefixlen_diff=1
def find_common_subnet2(subnets: Optional[list]) -> Optional[str]:
    # Assume, that all elements in the list are correct
    # Otherwise implement validation
    pass

    if not subnets:
        # Need to process situation, when input is empty
        # It was not mentioned in task, so return None
        return None

    if len(subnets) == 1:
        # if there is only one element, that it a answer
        return subnets[0]

    # Main logic
    # Parse subnets with ipaddress lib
    parsed = {ipaddress.ip_network(sub) for sub in subnets}
    # Get minimal prefixlen

    min_pref = min(p.prefixlen for p in parsed)
    # Algorith:
    # use the same conditions in while loop
    # but find parent network by using prefixlen_diff = 1
    # increase smallest subnets on 1 bit and check it
    while len(parsed) != 1 and min_pref > 1:
        tmp = set()
        tmp_low = set()
        for p in parsed:
            if p.prefixlen > min_pref:
                tmp_low.add(p.supernet())
            else:
                tmp.add(p)
        tmp.update(tmp_low)

        if not tmp_low:
            tmp = {p.supernet() for p in parsed}
        parsed = tmp
        min_pref = min(p.prefixlen for p in parsed)

    if len(parsed) != 1:
        # can not find common network
        return None

    return parsed.pop().exploded


if __name__ == '__main__':
    for pair in test_data:
        result = find_common_subnet(pair['in'])
#        print('\nINPUT:', pair['in'])
#        print('RESULT:', result)
        assert pair['out'] == result

        # first approach is shorter ad faster,
        # so the second is used just for demonstration another algorithm
        # DO NOT USE SECOND METHOD IN CODE :)
        result2 = find_common_subnet2(pair['in'])
        assert pair['out'] == result2
