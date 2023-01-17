import abc

class Source(metaclass=abc.ABCMeta):

  @abc.abstractmethod
  def wait_for_event(self):
    pass

  @abc.abstractmethod
  def start(self):
    pass

  @abc.abstractmethod
  def set_source_wrapper(self, source_wrapper):
    pass

  @abc.abstractmethod
  def event_success(self, exchange):
      pass

  # todo exchange with error
  @abc.abstractmethod
  def event_failure(self, err, exchange):
    pass
