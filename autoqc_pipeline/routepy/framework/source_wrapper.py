class SourceWrapper:

  def __init__(self, source, exchange_handler):
    self.__source = source
    self.__exchange_handler = exchange_handler

  def wait_for_events(self):
    while True:
      self.__exchange_handler.process(self.__source.wait_for_event())

  def start(self):
    return self.__source.start()