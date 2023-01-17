import os
import signal
from multiprocessing import Process, JoinableQueue

from PySide6 import QtCore, QtWidgets

from autoqc_pipeline.routepy.framework.exchange import Exchange
from autoqc_pipeline.routepy.framework.multi_process_joiner import \
  MultiProcessJoiner
from autoqc_pipeline.routepy.framework.source import Source



class FileSource(Source):

  DONE_FILE_PATH = 'DoneFilePath'

  def __init__(self, configuration):
    assert configuration.directory, 'directory parameter is required'
    self.__queue = JoinableQueue()
    self.__configuration = configuration
    self.__source_wrapper = None

  def set_source_wrapper(self, source_wrapper):
    self.__source_wrapper = source_wrapper

  def start(self):
    process = []
    supplier = Process(target=self.__source_wrapper.wait_for_events)
    supplier.daemon = True
    supplier.start()
    process.append(supplier)
    consumer = Process(target=self.run_app)
    consumer.daemon = True
    consumer.start()
    process.append(consumer)
    return MultiProcessJoiner(process)

  def __get_filter(self, ext_list):
    filter = []
    for ext in ext_list:
      filter.append('*.{}'.format(ext))
    return filter

  def run_app(self):
    app = QtCore.QCoreApplication([])
    signal.signal(signal.SIGINT, signal.SIG_DFL)
    self.watcher = QtWidgets.QFileSystemModel()
    self.watcher.setNameFilterDisables(False)
    if self.__configuration.done_file_ext:
      if self.__configuration.include_ext:
        exts = []
        for ext in self.__configuration.include_ext:
          exts.append('{}.{}'.format(ext, self.__configuration.done_file_ext))
        self.watcher.setNameFilters(self.__get_filter(exts))
      else:
        self.watcher.setNameFilters(self.__get_filter([self.__configuration.include_ext]))
    else:
      if self.__configuration.include_ext:
        self.watcher.setNameFilters(self.__get_filter(self.__configuration.include_ext))
    self.watcher.setRootPath(self.__configuration.directory)
    self.watcher.rowsInserted.connect(self.__rows_inserted)
    app.exec()

  def __rows_inserted(self, parent, first, last):
    for i in range(first, last + 1):
      child = self.watcher.index(i, 0, parent=parent)
      is_dir = self.watcher.isDir(child)
      if is_dir:
        if self.__configuration.recursive:
          self.watcher.fetchMore(child)
      else:
        path = self.watcher.filePath(child)
        if self.__configuration.done_file_ext:
          actual_path = path[0:( -1 * (len(self.__configuration.done_file_ext) + 1))]
          if not os.path.isfile(actual_path):
            # todo move to error location?
            os.remove(path)
            raise Exception("Done file found, but actual file does not exist: {}".format(actual_path))
          self.__queue.put(Exchange(actual_path).set_header(FileSource.DONE_FILE_PATH, path))
        else:
          self.__queue.put(Exchange(path))

  def wait_for_event(self):
    return self.__queue.get()

  def event_success(self, exchange):
    self.__queue.task_done()
    if exchange.get_header(FileSource.DONE_FILE_PATH):
      os.remove(exchange.get_header(FileSource.DONE_FILE_PATH))
    if self.__configuration.delete:
      os.remove(exchange.get_body())

  def event_failure(self, err, exchange):
    print(f"Unexpected {err=}, {type(err)=}")
    self.__queue.task_done()
    # todo move this file?
    if exchange.get_header(FileSource.DONE_FILE_PATH):
      os.remove(exchange.get_header(FileSource.DONE_FILE_PATH))
    # todo handle moving on error

