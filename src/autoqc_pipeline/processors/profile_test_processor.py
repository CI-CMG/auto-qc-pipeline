import os

from eipiphany_core.framework.base.processor import Processor

from .test_catalog import TestCatalog


class ProfileTestProcessor(Processor):

  def __init__(self, auto_qc_home, filter):
    self.__parameter_store = {}
    self.__auto_qc_home = auto_qc_home
    self.__filter = filter
    self.__tests = TestCatalog().get_test_info()
    cwd = os.getcwd()
    try:
      os.chdir(auto_qc_home)
      for test in self.__tests:
        test.load_parameters(self.__parameter_store)
    finally:
      os.chdir(cwd)

  def process(self, exchange):
    test_message = exchange.body
    if self.__filter.filter(exchange):
      profile = test_message.profile
      auto_qc_profile_test_result = test_message.profile_test_result
      cwd = os.getcwd()
      try:
        os.chdir(self.__auto_qc_home)
        for test in self.__tests:
          level_results = test.test(profile, self.__parameter_store).to_list()
          for depth in range(len(level_results)):
            if level_results[depth]:
              auto_qc_profile_test_result.profile_failures.add(test.name)
              auto_qc_profile_test_result.depth_failures[depth].add(test.name)
      finally:
        os.chdir(cwd)
    else:
      test_message.profile_test_result.skipped = True
