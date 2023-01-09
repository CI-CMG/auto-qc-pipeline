import pytest
import os
from uscg_split_survey.mapped_columns import MappedColumns
from uscg_split_survey.csv_header_reader import CsvHeaderReader

class TestHeaderReader:

  def test_read_header(self):
    print(os.getcwd())
    expected = MappedColumns(0,1,2,3)
    reader = CsvHeaderReader('data/test.xyz')
    assert expected == reader.get_mapped_columns()

  def test_read_empty_file(self):
    with pytest.raises(Exception) as e_info:
      reader = CsvHeaderReader('data/emptyfile.csv')
      reader.get_mapped_columns()