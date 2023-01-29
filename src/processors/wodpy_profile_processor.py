import os

from eipiphany_core.framework.base.processor import Processor
from eipiphany_core.message.exchange import Exchange
from wodpy import wod

from ..model.test_message import TestMessage


class WodpyProfileProcessor(Processor):

  def __init__(self, test_queue, *args, **kw):
    super().__init__(*args, **kw)
    self.__test_queue = test_queue


  def process(self, exchange):
    file_message = exchange.body
    try:
      with open(file_message.wod_file_path, 'r') as fid:
        while True:
          start = fid.tell()
          profile = wod.WodProfile(fid)
          end = fid.tell()
          fid.seek(start)
          fid.seek(end)
          last = profile.is_last_profile_in_file(fid)
          auto_qc_test_message = TestMessage(file_message.file_path_prefix, profile, last)
          self.__test_queue.put(Exchange(auto_qc_test_message), True)
          if last:
            break

    finally:
      os.remove(exchange.body.wod_file_path)
