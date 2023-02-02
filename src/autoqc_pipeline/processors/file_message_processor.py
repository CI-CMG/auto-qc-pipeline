import os

from eipiphany_core.framework.base.processor import Processor

from ..model.file_message import FileMessage


class FileMessageProcessor(Processor):


  def __splitall(self, path):
    allparts = []
    while 1:
      parts = os.path.split(path)
      if parts[0] == path:  # sentinel for absolute paths
        allparts.insert(0, parts[0])
        break
      elif parts[1] == path: # sentinel for relative paths
        allparts.insert(0, parts[1])
        break
      else:
        path = parts[0]
        allparts.insert(0, parts[1])
    return allparts

  def process(self, exchange):
    gzip_file_path = exchange.body
    path_list = self.__splitall(gzip_file_path)
    file_path_prefix = os.path.join(path_list[-3], path_list[-2], path_list[-1][:-3])
    exchange.body = FileMessage().set_gzip_file_path(gzip_file_path).set_file_path_prefix(file_path_prefix)
