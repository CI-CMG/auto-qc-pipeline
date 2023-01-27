class AutoQcFileResult(object):

  def __init__(self, file_path_prefix):
    self.__failure_counts = {}
    self.__total_casts = 0
    self.__file_path_prefix = file_path_prefix
    self.__complete = False
    self.__exception = None
    self.__exceptions = None

  @property
  def failure_counts(self):
    return self.__failure_counts

  @failure_counts.setter
  def failure_counts(self, failure_counts):
    self.set_failure_counts(failure_counts)

  def set_failure_counts(self, failure_counts):
    self.__failure_counts = failure_counts

  @property
  def total_casts(self):
    return self.__total_casts

  @total_casts.setter
  def total_casts(self, total_casts):
    self.set_total_casts(total_casts)

  def set_total_casts(self, total_casts):
    self.__total_casts = total_casts
    return self

  def increment_total_casts(self):
    self.__total_casts += 1

  @property
  def file_path_prefix(self):
    return  self.__file_path_prefix

  @file_path_prefix.setter
  def file_path_prefix(self, value):
    self.set_file_path_prefix(value)

  def set_file_path_prefix(self, value):
    self.__file_path_prefix = value
    return self

  @property
  def is_complete(self):
    return self.__complete

  @is_complete.setter
  def is_complete(self):
    self.set_is_complete()

  def set_is_complete(self):
    self.__complete = True
    return self

  @property
  def exception(self):
    return self.__exception

  @exception.setter
  def exception(self, exception):
    self.set_exception(exception)

  def set_exception(self, exception):
    self.__exception = exception
    return self

  @property
  def exceptions(self):
    return self.__exceptions

  @exceptions.setter
  def exceptions(self, exceptions):
    self.set_exceptions(self, exceptions)

  def set_exceptions(self, exceptions):
    self.__exceptions = exceptions
    return self

  def __str__(self):
    return 'AutoQcFileResult:' \
           '{{' \
           'total_casts={},' \
           '}}' \
      .format(
      self.__total_casts
    )
