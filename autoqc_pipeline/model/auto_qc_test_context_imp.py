from autoqc_pipeline.model.auto_qc_cast_test_result import AutoQcCastTestResult
from autoqc_pipeline.routepy.framework.auto_qc_test_context import \
  AutoQcTestContext


class AutoQcTestContextImpl(AutoQcTestContext):

  def __init__(self, file_path_prefix, last_cast, cast):
    self.__cast = cast
    self.__last_cast = False
    self.__file_path_prefix = file_path_prefix
    self.__cast_test_result = AutoQcCastTestResult(cast)

  @property
  def cast(self):
    return self.__cast

  @property
  def last_cast(self):
    return self.__last_cast

  @last_cast.setter
  def last_cast(self):
    self.set_last_cast()

  def set_last_cast(self):
    self.__last_cast = True
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
  def cast_test_result(self):
    return self.__cast_test_result

  @cast_test_result.setter
  def cast_test_result(self, cast_test_result):
    self.set_cast_test_result(cast_test_result)

  def set_cast_test_result(self, cast_test_result):
    self.__cast_test_result = cast_test_result
    return self
