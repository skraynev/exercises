from task_subnets import find_common_subnet
from task_subnets import test_data


def test_find_common_subnet():
    for pair in test_data:
        result = find_common_subnet(pair['in'])
        assert pair['out'] == result, '%s != %s' % (pair['out'], result)
