import gzip
import multiprocessing
import os
import shutil
from datetime import datetime
from pathlib import Path

from autoqc_pipeline.routepy.framework.processor import Processor


class GunzipProcessor2(Processor):

  def __init__(self, wod_directory, gunzip_directory, *args, **kw):
    super().__init__(*args, **kw)
    self.__wod_directory = wod_directory
    self.__gunzip_directory = gunzip_directory

  def process(self, exchange):
    process = multiprocessing.current_process()
    message = exchange.body
    gzip_path = message.gzip_file_path
    rel_path_split = os.path.split(os.path.relpath(gzip_path, start=self.__wod_directory))
    wod_file_path = os.path.join(self.__gunzip_directory, rel_path_split[0], rel_path_split[1][0:-3])
    Path(os.path.split(wod_file_path)[0]).mkdir( parents=True, exist_ok=True )
    message.wod_file_path = wod_file_path
    now = datetime.now().strftime("%Y-%m-%dT%H:%M:%M.%f")
    print("gunzip start {0} {1} {2}".format(now, process.pid, gzip_path))
    with gzip.open(gzip_path, 'rb') as f_in:
      with open(wod_file_path, 'wb') as f_out:
        shutil.copyfileobj(f_in, f_out)
    print("gunzip end {0} {1} {2}".format(now, process.pid, gzip_path))