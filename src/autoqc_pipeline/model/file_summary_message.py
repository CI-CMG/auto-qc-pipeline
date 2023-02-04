class FileSummaryMessage(object):

  def __init__(self, file_path_prefix):
    self.__failure_counts = {}
    self.__file_path_prefix = file_path_prefix
    self.__total_profiles = 0
    self.complete = False
    self.__exception_count = 0


  @property
  def failure_counts(self):
    return self.__failure_counts

  @property
  def file_path_prefix(self):
    return self.__file_path_prefix

  @property
  def total_profiles(self):
    return self.__total_profiles

  @property
  def is_complete(self):
    return self.complete

  @property
  def exception_count(self):
    return self.__exception_count

  def increment_total_profiles(self):
    self.__exception_count += 1

  def increment_exception_count(self):
    self.__total_profiles += 1

  def __str__(self):
    return 'AutoQcFileResult:' \
           '{{' \
           'file_path_prefix={},' \
           'total_casts={},' \
           '}}' \
      .format(
      self.__file_path_prefix,
      self.__total_casts
    )