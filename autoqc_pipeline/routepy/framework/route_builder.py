import abc

from autoqc_pipeline.routepy.framework.source_wrapper import SourceWrapper

class ExchangeHandler(object):
  def __init__(self):
    self.__processor = None
    self.__filter = None

  @property
  def processor(self):
    return self.__processor

  @processor.setter
  def processor(self, value):
    self.set_processor(value)

  def set_processor(self, value):
    self.__processor = value
    return self

  @property
  def filter(self):
    return self.__filter

  @filter.setter
  def filter(self, value):
    self.set_filter(value)

  def set_filter(self, value):
    self.__filter = value
    return self

class Route:

  def __init__(self, source):
    self.__source = source
    self.__source_wrapper = SourceWrapper(source, self)
    source.set_source_wrapper(self.__source_wrapper)
    self.__exchange_handlers = []

  # todo move this to separate class
  def process(self, exchange):
    try:
      for exchange_handler in self.__exchange_handlers:
        if exchange_handler.processor:
          exchange_handler.processor.process(exchange)
        elif exchange_handler.filter:
          keep_going = exchange_handler.filter.filter(exchange)
          if not keep_going:
            break
        else:
          raise Exception("Internal error: invalid exchange handler")
      self.__source.event_success(exchange)
    except Exception as err:
      self.__source.event_failure(err, exchange)

  def to(self, processor):
    self.__exchange_handlers.append(ExchangeHandler().set_processor(processor))
    return self

  def filter(self, filter):
    self.__exchange_handlers.append(ExchangeHandler().set_filter(filter))
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

