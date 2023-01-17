
class AutoQcMessage(object):
  def __init__(self):
    self.__gzip_file_path = None
    self.__wod_file_path = None
    self.__profile = None
    self.test_results = {}

  @property
  def gzip_file_path(self):
    return self.__gzip_file_path

  @gzip_file_path.setter
  def gzip_file_path(self, value):
    self.set_gzip_file_path(value)

  def set_gzip_file_path(self, value):
    self.__gzip_file_path = value
    return self

  @property
  def wod_file_path(self):
    return self.__wod_file_path

  @wod_file_path.setter
  def wod_file_path(self, value):
    self.set_wod_file_path(value)

  def set_wod_file_path(self, value):
    self.__wod_file_path = value
    return self

  @property
  def profile(self):
    return self.__profile

  @profile.setter
  def profile(self, value):
    self.set_profile(value)

  def set_profile(self, value):
    self.__profile = value
    return self

  def __str__(self):
    return 'AutoQcMessage:' \
           '{{' \
           'gzip_file_path={},' \
           'wod_file_path={}' \
           '}}' \
      .format(
      self.__gzip_file_path,
      self.__wod_file_path
    )