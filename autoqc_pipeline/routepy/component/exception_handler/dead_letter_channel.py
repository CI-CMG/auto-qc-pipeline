from autoqc_pipeline.routepy.framework.error_handler import ErrorHandler


class DeadLetterChannel(ErrorHandler):

  def __init__(self, endpoint):
    self.__endpoint = endpoint
    self.__prep_processor = None

  def on_prepare_failure(self, processor):
    self.__prep_processor = processor
    return self

  # todo hide this, move this
  def handle_exception(self, exchange):
    if self.__prep_processor:
      self.__prep_processor.process(exchange)
    self.__endpoint.process(exchange)




