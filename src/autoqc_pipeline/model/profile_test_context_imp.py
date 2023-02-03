from autoqc_pipeline.routepy.framework.auto_qc_test_context import \
  AutoQcTestContext
from src.autoqc_pipeline.model.test_message import ProfileTestResult


class AutoQcTestContextImpl(AutoQcTestContext):

  def __init__(self, file_path_prefix, last_profile, profile):
    self.__profile = profile
    self.__last_profile = False
    self.__file_path_prefix = file_path_prefix
    self.__profile_test_result = ProfileTestResult(profile)

  @property
  def profile(self):
    return self.__profile

  @property
  def last_profile(self):
    return self.__last_profile

  @last_profile.setter
  def last_profile(self):
    self.set_last_profile()

  def set_last_profile(self):
    self.__last_profile = True
    return self

  @property
  def file_path_prefix(self):
    return self.__file_path_prefix

  @file_path_prefix.setter
  def file_path_prefix(self, file_path_prefix):
    self.set_file_path_prefix(file_path_prefix)

  def set_file_path_prefix(self, file_path_prefix):
    self.__file_path_prefix = file_path_prefix
    return self

  @property
  def profile_test_result(self):
    return self.__profile_test_result

  @profile_test_result.setter
  def profile_test_result(self, profile_test_result):
    self.set_profile_test_result(profile_test_result)

  def set_profile_test_result(self, profile_test_result):
    self.__profile_test_result = profile_test_result
    return self
