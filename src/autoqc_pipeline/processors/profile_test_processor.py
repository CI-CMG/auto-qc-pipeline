import logging
import os

from eipiphany_core.framework.base.processor import Processor

from .dictionary_data_store import DictionaryDataStore

logger = logging.getLogger(__name__)

class ProfileTestProcessor(Processor):

  def __init__(self, auto_qc_home, filter, test_catalog):
    self.__parameter_store = {'cache_test_in_store':True}
    self.__auto_qc_home = auto_qc_home
    self.__filter = filter
    self.__initialized = False
    self.__test_catalog = test_catalog

  # This has to be called in the process method.  Calling in the constructor causes issues with multiprocessing
  def __initialize(self):
    cwd = os.getcwd()
    try:
      os.chdir(self.__auto_qc_home)
      for test in self.__test_catalog.get_test_info():
        test.load_parameters(self.__parameter_store)
    finally:
      os.chdir(cwd)
    self.__initialized = True

  def process(self, exchange):
    if not self.__initialized:
      self.__initialize()
    test_message = exchange.body
    if self.__filter.filter(exchange):
      profile = test_message.profile
      profile_test_result = test_message.profile_test_result
      cwd = os.getcwd()
      try:
        os.chdir(self.__auto_qc_home)
        data_store = DictionaryDataStore()
        for test in self.__test_catalog.get_test_info():
          print ("Running " + test.name)
          # logger.debug("Running " + test.name)
          level_results = test.test(profile, self.__parameter_store, data_store).tolist()
          for depth in range(len(level_results)):
            if level_results[depth]:
              profile_test_result.profile_failures.add(test.name)
              profile_test_result.depth_failures[depth].add(test.name)
      finally:
        os.chdir(cwd)
    else:
      test_message.profile_test_result.skipped = True
