import os

import qctests.AOML_gradient as AOML_gradient
import qctests.AOML_gross as AOML_gross
import qctests.AOML_spike as AOML_spike
import qctests.Argo_impossible_date_test as Argo_impossible_date_test
import qctests.Argo_impossible_location_test as Argo_impossible_location_test
import qctests.Argo_regional_range_test as Argo_regional_range_test
import qctests.EN_background_available_check as EN_background_available_check

from autoqc_pipeline.routepy.framework.processor import Processor

parameter_store = {
  # "table": dbtable,
  # "db": targetdb
}

class TestInfo(object):
  def __init__(self, name, module, has_parameters = False):
    self.name = name
    self.__module = module
    self.__has_parameters = has_parameters

  def load_parameters(self):
    if self.__has_parameters:
      self.__module.loadParameters(parameter_store)

  def test(self, profile):
    return self.__module.test(profile, parameter_store)


tests = [
  TestInfo('AOML_gross', AOML_gross),
  TestInfo('AOML_gradient', AOML_gradient),
  TestInfo('AOML_spike', AOML_spike),
  TestInfo('Argo_impossible_date_test', Argo_impossible_date_test),
  TestInfo('Argo_impossible_location_test', Argo_impossible_location_test),
  TestInfo('Argo_regional_range_test', Argo_regional_range_test),
  TestInfo('EN_background_available_check', EN_background_available_check, has_parameters=True)
]

cwd = os.getcwd()
try:
  auto_qc_home = os.environ['AUTO_QC_HOME']
  os.chdir(auto_qc_home)
  for test in tests:
    test.load_parameters()
finally:
  os.chdir(cwd)

class TestProcessor(Processor):


  def process(self, exchange):
    cwd = os.getcwd()
    try:
      auto_qc_home = os.environ['AUTO_QC_HOME']
      os.chdir(auto_qc_home)
      test_results = {}
      profile = exchange.get_body().profile
      for test in tests:
        test_results[test.name] = test.test(profile)
      exchange.get_body().test_results = test_results
    finally:
      os.chdir(cwd)