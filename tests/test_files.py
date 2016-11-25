# -*- coding: utf-8 -*-
"""
Created on Fri Nov 25 13:37:41 2016

@author: losoip
"""

import pytest

from context import files
from context import paths


_INVALID_FILENAME = 'invalid_filename'
_INVALID_PATH = 'invalid_path'
_VALID_PATH = paths._TESTS
_VALID_JSON = 'test_read.json'

_JSON_OBJECT = {'test_1': 1, 'test_2': 2}


class TestGetContent:

    def test_raise_filenotfounderror_invalid_filename(self):
        with pytest.raises(FileNotFoundError):
            files.get_content(_VALID_PATH, _INVALID_FILENAME)

    def test_raise_filenotfounderror_invalid_path(self):
        with pytest.raises(FileNotFoundError):
            files.get_content(_INVALID_PATH, _VALID_JSON)

    def test_raise_no_errors_valid_path_valid_filename(self):
        files.get_content(_VALID_PATH, _VALID_JSON)

    def test_raise_typeerror_invalid_filename(self):
        with pytest.raises(TypeError):
            files.get_content(_VALID_PATH, list(_VALID_JSON))

    def test_raise_typeerror_invalid_path(self):
        with pytest.raises(TypeError):
            files.get_content(list(_VALID_PATH), _VALID_JSON)

    def test_return_contains_only_strings(self):
        contents = files.get_content(_VALID_PATH, _VALID_JSON)
        for row in contents:
            assert isinstance(row, str)

    def test_return_list(self):
        contents = files.get_content(_VALID_PATH, _VALID_JSON)
        assert isinstance(contents, list)


class TestGetJson:

    def test_raise_filenotfounderror_invalid_filename(self):
        with pytest.raises(FileNotFoundError):
            files.get_json(_VALID_PATH, _INVALID_FILENAME)

    def test_raise_filenotfounderror_invalid_path(self):
        with pytest.raises(FileNotFoundError):
            files.get_json(_INVALID_PATH, _VALID_JSON)

    def test_raise_no_errors_valid_path_valid_filename(self):
        files.get_json(_VALID_PATH, _VALID_JSON)

    def test_raise_typeerror_invalid_filename(self):
        with pytest.raises(TypeError):
            files.get_json(_VALID_PATH, list(_VALID_JSON))

    def test_raise_typeerror_invalid_path(self):
        with pytest.raises(TypeError):
            files.get_json(list(_VALID_PATH), _VALID_JSON)

    def test_return_object(self):
        json_object = files.get_json(_VALID_PATH, _VALID_JSON)
        assert isinstance(json_object, object)

    def test_return_correct_object(self):
        json_object = files.get_json(_VALID_PATH, _VALID_JSON)
        assert json_object == _JSON_OBJECT


class TestWriteJson:

    filename = 'test_write.json'

    def test_output_file_exists(self):
        files.write_json(_JSON_OBJECT, _VALID_PATH, self.filename)
        output = files.get_json(_VALID_PATH, self.filename)
        assert isinstance(output, type(_JSON_OBJECT))

    def test_raise_typeerror_invalid_filename(self):
        with pytest.raises(TypeError):
            files.write_json(_JSON_OBJECT, _VALID_PATH, list(self.filename))

    def test_raise_no_errors_valid_path_valid_filename(self):
        files.write_json(_JSON_OBJECT, _VALID_PATH, self.filename)

    def test_raise_typeerror_invalid_path(self):
        with pytest.raises(TypeError):
            files.write_json(_JSON_OBJECT, list(_VALID_PATH), self.filename)

    def test_return_none(self):
        output = files.write_json(_JSON_OBJECT, _VALID_PATH, self.filename)
        assert isinstance(output, type(None))


class TestWriteJsons:

    filenames = ['test_write_1.json', 'test_write_2.json']
    data = [_JSON_OBJECT, _JSON_OBJECT]

    def test_output_files_exist(self):
        files.write_jsons(self.data, _VALID_PATH, self.filenames)
        for file, test_object in zip(self.filenames, self.data):
            output = files.get_json(_VALID_PATH, file)
            assert isinstance(output, type(test_object))

    def test_raise_no_errors_valid_data_path_filenames(self):
        files.write_jsons(self.data, _VALID_PATH, self.filenames)

    def test_raise_typeerror_invalid_data_type(self):
        with pytest.raises(TypeError):
            files.write_jsons(str(self.data), _VALID_PATH, self.filenames)

    def test_raise_typeerror_invalid_filenames_type(self):
        with pytest.raises(TypeError):
            files.write_jsons(self.data, _VALID_PATH, str(self.filenames))

    def test_raise_typeerror_invalid_path(self):
        with pytest.raises(TypeError):
            files.write_jsons(self.data, list(_VALID_PATH), self.filenames)

    def test_return_none(self):
        output = files.write_jsons(self.data, _VALID_PATH, self.filenames)
        assert isinstance(output, type(None))
