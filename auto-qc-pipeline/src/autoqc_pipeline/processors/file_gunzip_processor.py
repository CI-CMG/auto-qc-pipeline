import gzip
import logging
import os
import shutil
from datetime import datetime
from pathlib import Path

from eipiphany_core.framework.base.processor import Processor

logger = logging.getLogger('autoqc.FileGunzipProcessor')

class FileGunzipProcessor(Processor):

  def __init__(self, wod_directory, gunzip_directory, output_dir, *args, **kw):
    super().__init__(*args, **kw)
    self.__wod_directory = wod_directory
    self.__gunzip_directory = gunzip_directory
    self.__output_dir = output_dir

  def process(self, exchange):
    file_message = exchange.body
    gzip_path = file_message.gzip_file_path
    rel_path_split = os.path.split(os.path.relpath(gzip_path, start=self.__wod_directory))
    wod_file_path = os.path.join(self.__gunzip_directory, rel_path_split[0], rel_path_split[1][0:-3])
    Path(os.path.split(wod_file_path)[0]).mkdir( parents=True, exist_ok=True )
    file_message.wod_file_path = wod_file_path
    now = datetime.now().strftime("%Y-%m-%dT%H:%M:%M.%f")
    logger.info("gunzip start {0} {1}".format(now, gzip_path))
    with gzip.open(gzip_path, 'rb') as f_in:
      with open(wod_file_path, 'wb') as f_out:
        shutil.copyfileobj(f_in, f_out)
    logger.info("gunzip end {0} {1}".format(now, gzip_path))
    results_dir = os.path.join(self.__output_dir, file_message.file_path_prefix + "-QC")
    if os.path.exists(results_dir):
      shutil.rmtree(results_dir, ignore_errors=True)
    Path(results_dir).mkdir( parents=True, exist_ok=True )
    logger.debug("Created {0}".format(results_dir))