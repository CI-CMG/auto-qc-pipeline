import logging
import os
import time

from eipiphany_core.framework.base.processor import Processor

from .dictionary_data_store import DictionaryDataStore
from .geohash_buddy_finder import GeohashBuddyFinder

logger = logging.getLogger('autoqc.ProfileTestProcessor')

class ProfileTestProcessor(Processor):

  def __init__(self, auto_qc_home, filter, test_catalog, geohash_service, gunzip_directory):
    self.__parameter_store = {'cache_test_in_store':True}
    self.__auto_qc_home = auto_qc_home
    self.__filter = filter
    self.__initialized = False
    self.__test_catalog = test_catalog
    self.__geohash_service = geohash_service
    self.__gunzip_directory = gunzip_directory

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
    start = time.time()
    test_message = exchange.body
    profile = test_message.profile
    if self.__filter.assess_profile(profile):
      profile_test_result = test_message.profile_test_result
      cwd = os.getcwd()
      try:
        os.chdir(self.__auto_qc_home)
        data_store = DictionaryDataStore()
        parameter_store = self.__parameter_store.copy()
        parameter_store['buddy_finder'] = GeohashBuddyFinder(self.__geohash_service, self.__gunzip_directory, test_message)
        for test in self.__test_catalog.get_test_info():
          # logger.debug("Running " + test.name)
          level_results = test.test(profile, parameter_store, data_store).tolist()
          for depth in range(len(level_results)):
            if level_results[depth]:
              profile_test_result.profile_failures.add(test.name)
              profile_test_result.depth_failures[depth].add(test.name)
      finally:
        os.chdir(cwd)
    else:
      test_message.profile_test_result.skipped = True
    end = time.time()
    print("profile {}/{} tested in {} sec.".format(test_message.file_path_prefix, str(profile.uid()), str(end - start)))
