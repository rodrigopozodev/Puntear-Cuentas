import pandas as pd
import os
import pytest
from utils.excel_reader import read_excel

def test_read_excel_valid_file():
    # Test reading a valid Excel file
    file_path = os.path.join(os.path.dirname(__file__), 'test_data', 'valid_file.xlsx')
    data = read_excel(file_path)
    assert isinstance(data, list)
    assert len(data) > 0

def test_read_excel_invalid_file():
    # Test reading an invalid Excel file
    file_path = os.path.join(os.path.dirname(__file__), 'test_data', 'invalid_file.xlsx')
    with pytest.raises(Exception):
        read_excel(file_path)

def test_read_excel_empty_file():
    # Test reading an empty Excel file
    file_path = os.path.join(os.path.dirname(__file__), 'test_data', 'empty_file.xlsx')
    data = read_excel(file_path)
    assert data == []