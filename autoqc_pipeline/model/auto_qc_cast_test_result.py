class AutoQcCastTestResult(object):

  def __init__(self, cast):
    self.__cast_failures = {}
    self.__depth_failures = [{} for _ in range(cast.get_depth_size())]
    self.__skipped = False
    self.__skip_reason = None
    self.__exception = None

  def get_depth_failures(self):
    return self.__depth_failures

  def get_cast_failures(self):
    return self.__cast_failures

  def is_failed(self):
    return not bool(self.__cast_failures) or self.__exception is not None

  def is_skipped(self):
    return self.__skipped

  def set_skipped(self, skipped):
    self.__skipped = skipped

  def get_skip_reason(self):
    return self.__skip_reason

  def set_skip_reason(self, skip_reason):
    self.__skip_reason = skip_reason

  def get_exception(self):
    return self.__exception

  def set_exception(self, exception):
    self.__exception = exception

