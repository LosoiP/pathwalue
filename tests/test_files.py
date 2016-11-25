# -*- coding: utf-8 -*-
"""
Created on Fri Nov 25 13:37:41 2016

@author: losoip
"""

import pytest

from context import files


class TestGetContent:

    invalid_filename = 'invalid_filename.txt'
    invalid_path = 'invalid_path'
    valid_filename = m.RHEA_EC
    valid_path = m.PATH_RHEA

    def test_output_contains_strings(self):
        output = m.get_content(self.valid_path, self.valid_filename)
        for item in output:
            assert isinstance(item, str)

    def test_output_is_list(self):
        output = m.get_content(self.valid_path, self.valid_filename)
        assert isinstance(output, list)

    def test_raise_filenotfounderror_invalid_filename(self):
        with pytest.raises(FileNotFoundError):
            m.get_content(self.valid_path, self.invalid_filename)

    def test_raise_filenotfounderror_invalid_path(self):
        with pytest.raises(FileNotFoundError):
            m.get_content(self.invalid_path, self.valid_filename)

    def test_raise_no_errors_valid_path_valid_filename(self):
        m.get_content(self.valid_path, self.valid_filename)

    def test_raise_typeerror_invalid_filename(self):
        with pytest.raises(TypeError):
            m.get_content(self.valid_path, list(self.valid_filename))

    def test_raise_typeerror_invalid_path(self):
        with pytest.raises(TypeError):
            m.get_content(list(self.valid_path), self.valid_filename)


class TestGetJson:

    invalid_filename = 'invalid_filename.txt'
    invalid_path = 'invalid_path'
    valid_filename = m.FILE_CMP_REACTIONS
    valid_path = m.PATH_JSON

    def test_output_is_object(self):
        output = m.get_json(self.valid_path, self.valid_filename)
        assert isinstance(output, object)

    def test_raise_filenotfounderror_invalid_filename(self):
        with pytest.raises(FileNotFoundError):
            m.get_json(self.valid_path, self.invalid_filename)

    def test_raise_filenotfounderror_invalid_path(self):
        with pytest.raises(FileNotFoundError):
            m.get_json(self.invalid_path, self.valid_filename)

    def test_raise_no_errors_valid_path_valid_filename(self):
        m.get_json(self.valid_path, self.valid_filename)

    def test_raise_typeerror_invalid_filename(self):
        with pytest.raises(TypeError):
            m.get_json(self.valid_path, list(self.valid_filename))

    def test_raise_typeerror_invalid_path(self):
        with pytest.raises(TypeError):
            m.get_json(list(self.valid_path), self.valid_filename)


class TestWriteJson:

    filename = 'test1.txt'
    path = m.PATH_JSON
    data_object = {}

    def test_output_file_exists(self):
        m.write_json(self.data_object, self.path, self.filename)
        output = m.get_json(self.path, self.filename)
        assert isinstance(output, type(self.data_object))

    def test_raise_typeerror_invalid_filename(self):
        with pytest.raises(TypeError):
            m.write_json(self.data_object, self.path, list(self.filename))

    def test_raise_no_errors_valid_path_valid_filename(self):
        m.write_json(self.data_object, self.path, self.filename)

    def test_raise_typeerror_invalid_path(self):
        with pytest.raises(TypeError):
            m.write_json(self.data_object, list(self.path), self.filename)

    def test_return_none(self):
        output = m.write_json(self.data_object, self.path, self.filename)
        assert isinstance(output, type(None))


class TestWriteJsons:

    filenames = ['test1.txt', 'test2.txt']
    path = m.PATH_JSON
    data = [{}, {}]

    def test_output_files_exist(self):
        m.write_jsons(self.data, self.path, self.filenames)
        for file, test_object in zip(self.filenames, self.data):
            output = m.get_json(self.path, file)
            assert isinstance(output, type(test_object))

    def test_raise_no_errors_valid_data_path_filenames(self):
        m.write_jsons(self.data, self.path, self.filenames)

    def test_raise_typeerror_invalid_data_type(self):
        with pytest.raises(TypeError):
            m.write_jsons(str(self.data), self.path, self.filenames)

    def test_raise_typeerror_invalid_filenames_type(self):
        with pytest.raises(TypeError):
            m.write_jsons(self.data, self.path, str(self.filenames))

    def test_raise_typeerror_invalid_path(self):
        with pytest.raises(TypeError):
            m.write_jsons(self.data, list(self.path), self.filenames)

    def test_return_none(self):
        output = m.write_jsons(self.data, self.path, self.filenames)
        assert isinstance(output, type(None))
