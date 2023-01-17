import abc

from autoqc_pipeline.routepy.framework.source_wrapper import SourceWrapper


class Route:

  def __init__(self, source):
    self.__source = source
    self.__source_wrapper = SourceWrapper(source, self)
    source.set_source_wrapper(self.__source_wrapper)
    self.__processors = []

  # todo move this to separate class
  def process(self, exchange):
    try:
      for processor in self.__processors:
        processor.process(exchange)
      self.__source.event_success(exchange)
    except Exception as err:
      self.__source.event_failure(err, exchange)

  def to(self, processor):
    self.__processors.append(processor)
    return self

  def start(self):
    return self.__source_wrapper.start()

class RouteBuilder(metaclass=abc.ABCMeta):

  def __init__(self):
    self.__routes = []

  def comes_from(self, source):
    route = Route(source)
    self.__routes.append(route)
    return route

  @abc.abstractmethod
  def build(self):
    pass

  def get_routes(self):
    return self.__routes

  def start(self):
    joiners = []
    for route in self.__routes:
      joiners.append(route.start())
    return joiners

