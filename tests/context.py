# -*- coding: utf-8 -*-
# (C) 2017 Tampere University of Technology
# MIT License
# Pauli Losoi
"""
Define context for unit test modules.

Each of the test_*.py modules import from this context module. This is
to enable easier use of the pytest testing tool within the tests
directory.

"""

import os
import sys

sys.path.insert(0, os.path.normpath('../python/'))

import chebi
import files
import intenz
# import main
import market
import paths
import pw
import rhea
