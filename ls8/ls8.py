#!/usr/bin/env python3

"""Main."""

import sys
# from cpu import *
from cpu1 import *

cpu = CPU()

cpu.load(sys.argv[1])
cpu.run()

# use: python ls8.py examples/print8.ls8
#            argv[0]       argv[1]