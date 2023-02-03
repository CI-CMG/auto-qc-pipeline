import os

from eipiphany_core.framework.base.processor import Processor
from eipiphany_core.message.exchange import Exchange
from wodpy import wod

from ..model.test_message import TestMessage


class WodpyProfileProcessor(Processor):

  def __init__(self, eip_context, file_controller, *args, **kw):
    super().__init__(*args, **kw)
    self.__test_queue_producer = eip_context.get_endpoint('seda:test-queue')
    self.__file_controller = file_controller


  def process(self, exchange):
    file_message = exchange.body
    try:
      with open(file_message.wod_file_path, 'r') as fid:
        file_path_prefix = file_message.file_path_prefix
        self.__file_controller.on_new_file(file_path_prefix)
        while True:
          profile = wod.WodProfile(fid)
          last = profile.is_last_profile_in_file(fid)
          self.__file_controller.on_new_cast(file_path_prefix, profile.uid(), last)
          auto_qc_test_message = TestMessage(file_message.file_path_prefix, profile, last)
          self.__test_queue_producer.process(Exchange(auto_qc_test_message), None)
          if last:
            break
    finally:
      os.remove(exchange.body.wod_file_path)
