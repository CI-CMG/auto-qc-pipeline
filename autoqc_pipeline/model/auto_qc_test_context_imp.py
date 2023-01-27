from autoqc_pipeline.model.auto_qc_cast_test_result import AutoQcCastTestResult
from autoqc_pipeline.routepy.framework.auto_qc_test_context import \
  AutoQcTestContext


class AutoQcTestContextImpl(AutoQcTestContext):

  def __init__(self, file_path_prefix, last_cast, cast):
    self.__cast = cast
    self.__last_cast = last_cast
    self.__file_path_prefix = file_path_prefix
    self.__cast_test_result = AutoQcCastTestResult(cast)

  def get_cast(self):
    return self.__cast

  def is_last_cast(self):
    return self.__last_cast

  def set_last_cast(self, last_cast):
    self.__last_cast = last_cast

  def get_file_path_prefix(self):
    return self.__file_path_prefix

  def set_file_path_prefix(self, file_path_prefix):
    self.__file_path_prefix = file_path_prefix

  def get_cast_test_result(self):
    return self.__cast_test_result

  def set_cast_test_result(self, cast_test_result):
    self.__cast_test_result = cast_test_result
