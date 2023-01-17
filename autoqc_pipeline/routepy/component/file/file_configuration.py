
class FileSourceConfiguration(object):
  def __init__(self):
    self.__directory = None
    self.__recursive = False
    self.__include_ext = []
    self.__done_file_ext = None
    self.__delete = False
    # self.__noop = True

  @property
  def directory(self):
    return self.__directory

  @directory.setter
  def directory(self, value):
    self.set_directory(value)

  def set_directory(self, value):
    self.__directory = value
    return self

  @property
  def recursive(self):
    return self.__recursive

  @recursive.setter
  def recursive(self, value):
    self.set_recursive(value)

  def set_recursive(self, value):
    self.__recursive = value
    return self

  @property
  def include_ext(self):
    return self.__include_ext

  @include_ext.setter
  def include_ext(self, value):
    self.set_include_ext(value)

  def set_include_ext(self, value):
    if value:
      self.__include_ext = value
    else:
      self.__include_ext = []
    return self

  @property
  def done_file_ext(self):
    return self.__done_file_ext

  @done_file_ext.setter
  def done_file_ext(self, value):
    self.set_done_file_ext(value)

  def set_done_file_ext(self, value):
    self.__done_file_ext = value
    return self

  # @property
  # def noop(self):
  #   return self.__include_ext
  #
  # @noop.setter
  # def noop(self, value):
  #   self.__noop = value
  #   return self
  #
  # def set_noop(self, value):
  #   self.__noop = value
  #   return self

  @property
  def delete(self):
    return self.__delete

  @delete.setter
  def delete(self, value):
    self.set_directory(value)

  def set_delete(self, value):
    self.__delete = value
    return self

  # todo
  def __str__(self):
    return 'FileSourceConfiguration:' \
           '{{' \
           'directory={},' \
           'recursive={}' \
           '}}'\
      .format(
      self.__directory,
      self.__recursive
    )