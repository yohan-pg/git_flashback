import sys

import git_flashback 
from git_flashback import *

import tests

with flashback("20220521T004912"): 
    # print(sys.modules)
    import tests as old_tests
    # import tests
    print(tests == old_tests) # type: ignore