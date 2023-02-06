class FileController(object):

  def __init__(self, manager):
    self.__profiles_in_flight = manager.dict()
    self.__lock = manager.RLock()

  def reset(self):
    self.__lock.acquire()
    try:
      self.__profiles_in_flight.clear()
    finally:
      self.__lock.release()

  def get_context(self, file_path_prefix):
    self.__lock.acquire()
    try:
      self.__profiles_in_flight.get(file_path_prefix)
    finally:
      self.__lock.release()

  def on_new_file(self, file_path_prefix):
    self.__lock.acquire()
    try:
      self.__profiles_in_flight[file_path_prefix] = ProfileProcessingContext()
    finally:
      self.__lock.release()

  def on_new_profile(self, file_path_prefix, profile_num, last):
    self.__lock.acquire()
    try:
      context = self.__profiles_in_flight.get(file_path_prefix)
      if context is not None:
        context.profiles.append(profile_num)
      if last:
        context.set_is_complete()
      self.__profiles_in_flight[file_path_prefix] = context
    finally:
      self.__lock.release()

  def on_done_profile(self, file_path_prefix, profile_num):
    self.__lock.acquire()
    try:
      context = self.__profiles_in_flight.get(file_path_prefix)
      if context is None:
        return True
      done = False
      context.profiles.remove(profile_num)
      self.__profiles_in_flight[file_path_prefix] = context
      if context.is_complete and not context.profiles:
        done = True
        self.__profiles_in_flight.pop(file_path_prefix, None)
      return done
    finally:
      self.__lock.release()

class ProfileProcessingContext(object):

  def __init__(self):
    self.__profiles = []
    self.__complete = False

  @property
  def profiles(self):
    return self.__profiles

  @property
  def is_complete(self):
    return self.__complete

  @is_complete.setter
  def is_complete(self):
    self.set_is_complete()

  def set_is_complete(self):
    self.__complete = True
    return self


