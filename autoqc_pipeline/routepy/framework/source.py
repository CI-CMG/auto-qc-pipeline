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
