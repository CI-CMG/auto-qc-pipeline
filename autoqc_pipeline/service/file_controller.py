class FileController(object):

  def __init__(self, manager):
    self.__casts_in_flight = manager.dict()
    self.__lock = manager.RLock()

  def reset(self):
    self.__lock.acquire()
    try:
      self.__casts_in_flight.clear()
    finally:
      self.__lock.release()

  def get_context(self, file_path_prefix):
    self.__lock.acquire()
    try:
      self.__casts_in_flight.get(file_path_prefix)
    finally:
      self.__lock.release()

  def on_new_file(self, file_path_prefix):
    self.__lock.acquire()
    try:
      self.__casts_in_flight[file_path_prefix] = self.CastProcessingContext()
    finally:
      self.__lock.release()

  def on_new_cast(self, file_path_prefix, cast_num, last):
    self.__lock.acquire()
    try:
      context = self.__casts_in_flight.get(file_path_prefix)
      if context is not None:
        context.casts.append(cast_num)
      if last:
        context.set_complete()
    finally:
      self.__lock.release()

  def on_done_cast(self, file_path_prefix, cast_num):
    self.__lock.acquire()
    try:
      context = self.__casts_in_flight.get(file_path_prefix)
      if context is None:
        return True
      done = False
      context.casts.remove(cast_num)
      if context.is_complete and bool(context.casts):
        done = True
        self.__casts_in_flight.pop(file_path_prefix, None)
      return done
    finally:
      self.__lock.release()

  class CastProcessingContext(object):

    def __init__(self):
      self.__casts = []
      self.__complete = False

    @property
    def casts(self):
      return self.__casts

    @property
    def is_complete(self):
      return self.__complete

    def set_complete(self):
      self.__complete = True


