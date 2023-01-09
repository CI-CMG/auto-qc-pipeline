import pytest
from autoqc_pipeline.example import Example

class TestHeaderReader:

  def test(self):
    example = Example()
    assert 'stuff' == example.do_stuff()
