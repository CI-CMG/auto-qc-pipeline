import copy
import os

from wodpy import wod

from autoqc_pipeline.model.auto_qc_test_context_imp import AutoQcTestContextImpl
from autoqc_pipeline.routepy.framework.processor import Processor


class WodpyProcessor(Processor):

  def __init__(self, test_queue, file_controller, *args, **kw):
    super().__init__(*args, **kw)
    self.__test_queue = test_queue
    self.__file_controller = file_controller


  def process(self, exchange):
    try:
      with open(exchange.get_body().wod_file_path, 'r') as fid:
        file_path_prefix = exchange.get_body().file_path_prefix
        self.__file_controller.on_new_file(file_path_prefix)
        while True:
          start = fid.tell()
          profile = wod.WodProfile(fid)
          end = fid.tell()
          fid.seek(start)
          fid.seek(end)
          profile_message = copy.copy(exchange.get_body())
          profile_message.profile = profile
          last = profile.is_last_profile_in_file(fid)
          self.__file_controller.on_new_cast(file_path_prefix, profile.uid(), last)
          self.__test_queue.put(profile_message, True)
          if last:
            break

    finally:
      os.remove(exchange.get_body().wod_file_path)
