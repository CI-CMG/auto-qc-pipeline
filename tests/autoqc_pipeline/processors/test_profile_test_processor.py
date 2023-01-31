import os

from eipiphany_core.message.exchange import Exchange

from src.autoqc_pipeline.filters.pathological_profile_filter import \
  PathologicalProfilesFilter
from src.autoqc_pipeline.processors.file_gunzip_processor import \
  FileGunzipProcessor
from src.autoqc_pipeline.processors.file_message_processor import \
  FileMessageProcessor
from src.autoqc_pipeline.processors.profile_test_processor import \
  ProfileTestProcessor
from src.autoqc_pipeline.processors.wodpy_profile_processor import \
  WodpyProfileProcessor


class MockQueue(object):
  def __init__(self):
    self.__exchanges = []

  def put(self, exchange, block):
    self.__exchanges.append(exchange)

  @property
  def exchanges(self):
    return self.__exchanges

class TestProfileTestProcessor(object):

  def test_process(self):
    root = os.environ['AUTO_QC_PIPELINE_ROOT']
    wod_directory = root + '/test-resources/wod18'
    gunzip_directory = root + '/gunzip-dir'
    output_directory = root + '/test-dir'
    auto_qc_home = os.environ['AUTO_QC_HOME']

    exchange = Exchange(root + '/test-resources/wod18/CTD/OBS/CTDO1977.gz')

    FileMessageProcessor().process(exchange)
    FileGunzipProcessor(wod_directory, gunzip_directory).process(exchange)

    mock_queue = MockQueue()
    exchanges = mock_queue.exchanges
    WodpyProfileProcessor(mock_queue).process(exchange)

    test_processor = ProfileTestProcessor(auto_qc_home, PathologicalProfilesFilter())
    for split_exchange in exchanges:
      test_processor.process(split_exchange)


