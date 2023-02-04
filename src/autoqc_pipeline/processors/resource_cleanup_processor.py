import os
import shutil

from eipiphany_core.framework.base.processor import Processor


class ResourceCleanupProcessor(Processor):

  def __init__(self, gunzip_directory):
    self.__gunzip_directory = gunzip_directory

  def process(self, exchange):
    message = exchange.body
    file_path_prefix = message.file_path_prefix
    wod_file = os.path.join(self.__gunzip_directory, file_path_prefix)
    hash_dir = os.path.join(self.__gunzip_directory, file_path_prefix + '.geohash')

    if os.path.exists(wod_file):
      os.remove(wod_file)

    if os.path.exists(hash_dir):
      shutil.rmtree(hash_dir, ignore_errors=True)
