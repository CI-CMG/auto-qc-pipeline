import copy
import os

from wodpy import wod

from autoqc_pipeline.routepy.framework.processor import Processor


class WodpyProcessor(Processor):

  def __init__(self, test_queue, *args, **kw):
    super().__init__(*args, **kw)
    self.__test_queue = test_queue


  def process(self, exchange):
    try:
      with open(exchange.get_body().wod_file_path, 'r') as fid:
        while True:
          start = fid.tell()
          profile = wod.WodProfile(fid)
          end = fid.tell()
          fid.seek(start)
          fid.seek(end)
          profile_message = copy.copy(exchange.get_body())
          profile_message.profile = profile
          self.__test_queue.put(profile_message, True)
          if profile.is_last_profile_in_file(fid):
            break
    finally:
      os.remove(exchange.get_body().wod_file_path)
