from eipiphany_core.framework.base.processor import Processor

from .test_catalog import HTPR, Comp, LFPR


class IquodFlagProcessor(Processor):

  def __init__(self, test_catalog):
    self.__test_catalog = test_catalog
    self.__htpr_tests = self.__test_catalog.get_test_names_for_set(HTPR)
    self.__comp_tests = self.__test_catalog.get_test_names_for_set(Comp)
    self.__lfpr_tests = self.__test_catalog.get_test_names_for_set(LFPR)

  def process(self, exchange):
    test_message = exchange.body
    test_result = test_message.profile_test_result
    failed_test_sets = []
    for test_failures in test_result.depth_failures:
      failed_test_sets.append(self.__get_depth_failure_test_set(test_failures))
    is_xbt = test_message.profile.probe_type() == 2
    flags = self.__gen_flags(failed_test_sets, is_xbt)
    test_result.iquod_flags = flags

  def __get_depth_failure_test_set(self, test_failures):
    test_set = set()
    if not self.__htpr_tests.isdisjoint(test_failures):
      test_set.add(HTPR)
    if not self.__comp_tests.isdisjoint(test_failures):
      test_set.add(Comp)
    if not self.__lfpr_tests.isdisjoint(test_failures):
      test_set.add(LFPR)
    return test_set

  def __gen_flags(self, failed_test_sets, is_xbt):
    '''
    given per-level lists of results for each of HTPR, Comp and LFPR cases,
    assess the appropriate IQuOD flag per our paper's prescription
    if isXBT, flags should be monotonically increasing with depth, meaning higher flags propagate to all deeper levels
    '''

    flags = []
    min_flag = 1
    for test_sets in failed_test_sets:
      flag = min_flag
      if LFPR in test_sets:
        flag = max(4, min_flag)
        if is_xbt: min_flag = max(4, min_flag)
      elif Comp in test_sets:
        flag = max(3, min_flag)
        if is_xbt: min_flag = max(3, min_flag)
      elif HTPR in test_sets:
        flag = max(2, min_flag)
        if is_xbt: min_flag = max(2, min_flag)
      flags.append(flag)
    return flags
