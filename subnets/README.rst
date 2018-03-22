TODO:

Given a list of IPv4 subnets, compute the smallest IPv4 subnet that contains
all given subnets.

Solution:

script is written and checked on python3.5
Old versions of Python is not supported due to type hints in function
definition.

Run script in virtualenv with python3:

.. code-block:: bash

    python3 task_subnet.py

# NOTE: running task_subnet.py execute test examples and do simple validation,
        so for it combinate sorce code and simple test in the same file.
        For re-using method in the module somewhere, please remove extra method,
        testcases and "__main__" method.

Run test module by using pytest:

.. code-block:: bash

    pip install pytest
    pytest test_subnet.py
    flake8 test_subnet.py

# NOTE: current method does not interact with any extarnal service or process,
        so there is not any mock objects inside test module.
