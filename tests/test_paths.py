# -*- coding: utf-8 -*-
"""
Created on Fri Nov 25 13:37:56 2016

@author: losoip
"""

import pytest

from context import paths


class TestGetNames:

    invalid_path = 'invalid_path'
    valid_path = paths._TESTS

    def test_raise_directorynotfounderror_invalid_path(self):
        with pytest.raises(paths.DirectoryNotFoundError):
            paths.get_names(self.invalid_path)

    def test_raise_no_errors_valid_path(self):
        paths.get_names(self.valid_path)

    def test_raise_typeerror_invalid_path(self):
        with pytest.raises(TypeError):
            paths.get_names(list(self.invalid_path))

    def test_return_contains_only_strings(self):
        filenames = paths.get_names(self.valid_path)
        for name in filenames:
            assert isinstance(name, str)

    def test_return_list(self):
        filenames = paths.get_names(self.valid_path)
        assert isinstance(filenames, list)

    def test_return_test_paths_py(self):
        filenames = paths.get_names(self.valid_path)
        assert 'test_paths.py' in filenames
