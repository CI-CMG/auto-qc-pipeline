
class FileMessage(object):
  def __init__(self):
    self.__gzip_file_path = None
    self.__wod_file_path = None
    self.__file_path_prefix = None

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
  def file_path_prefix(self):
    return  self.__file_path_prefix

  @file_path_prefix.setter
  def file_path_prefix(self, value):
    self.set_file_path_prefix(value)

  def set_file_path_prefix(self, value):
    self.__file_path_prefix = value
    return self
