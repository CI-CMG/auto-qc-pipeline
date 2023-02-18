from eipiphany_core.message.exchange import Exchange

from src.autoqc_pipeline.model.test_message import TestMessage
from src.autoqc_pipeline.processors.iquod_flag_processor import IquodFlagProcessor

HTPR = 'HTPR'
Comp = 'Comp'
LFPR = 'LFPR'

class MockTestCatalog(object):
  def get_test_names_for_set(self, test_set):
    if test_set == HTPR:
      return {'Test1', 'Test2', 'Test3'}
    elif test_set == Comp:
      return {'Test1', 'Test4', 'Test3'}
    elif test_set == LFPR:
      return {'Test1', 'Test6', 'Test7'}
    else:
      raise Exception("Invalid test set")

class MockProfile(object):
  def __init__(self, probe_type=1.0, n_levels=3):
    self.__probe_type = probe_type
    self.__n_levels = n_levels

  def probe_type(self):
    return self.__probe_type

  def n_levels(self):
    return self.__n_levels


class TestIquodFlagProcessor(object):


  def test_basic(self):
    test_catalog = MockTestCatalog()
    processor = IquodFlagProcessor(test_catalog)
    file_path_prefix = "foo/bar"
    last_profile = False
    geohash = "abc"
    profile = MockProfile()
    test_message = TestMessage(file_path_prefix, profile, last_profile, geohash)
    level_0 = test_message.profile_test_result.depth_failures[0]
    level_1 = test_message.profile_test_result.depth_failures[1]
    level_2 = test_message.profile_test_result.depth_failures[2]
    level_0.add("Test2")
    level_1.add("Test4")
    level_2.add("Test6")
    exchange = Exchange(test_message)
    processor.process(exchange)
    iquod_flags = test_message.profile_test_result.iquod_flags
    assert len(iquod_flags) == 3
    assert iquod_flags[0] == 2
    assert iquod_flags[1] == 3
    assert iquod_flags[2] == 4

  def test_duplicate_test_highest(self):
    test_catalog = MockTestCatalog()
    processor = IquodFlagProcessor(test_catalog)
    file_path_prefix = "foo/bar"
    last_profile = False
    geohash = "abc"
    profile = MockProfile()
    test_message = TestMessage(file_path_prefix, profile, last_profile, geohash)
    level_0 = test_message.profile_test_result.depth_failures[0]
    level_1 = test_message.profile_test_result.depth_failures[1]
    level_0.add("Test1")
    level_1.add("Test3")
    exchange = Exchange(test_message)
    processor.process(exchange)
    iquod_flags = test_message.profile_test_result.iquod_flags
    assert len(iquod_flags) == 3
    assert iquod_flags[0] == 4
    assert iquod_flags[1] == 3
    assert iquod_flags[2] == 1

  def test_xbt(self):
    test_catalog = MockTestCatalog()
    processor = IquodFlagProcessor(test_catalog)
    file_path_prefix = "foo/bar"
    last_profile = False
    geohash = "abc"
    profile = MockProfile(probe_type=2.0)
    test_message = TestMessage(file_path_prefix, profile, last_profile, geohash)
    level_0 = test_message.profile_test_result.depth_failures[0]
    level_1 = test_message.profile_test_result.depth_failures[1]
    level_2 = test_message.profile_test_result.depth_failures[2]
    level_0.add("Test2")
    level_1.add("Test6")
    level_2.add("Test4")
    exchange = Exchange(test_message)
    processor.process(exchange)
    iquod_flags = test_message.profile_test_result.iquod_flags
    assert len(iquod_flags) == 3
    assert iquod_flags[0] == 2
    assert iquod_flags[1] == 4
    assert iquod_flags[2] == 4
