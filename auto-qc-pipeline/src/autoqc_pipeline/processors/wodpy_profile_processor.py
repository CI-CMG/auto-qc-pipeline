from eipiphany_core.framework.base.processor import Processor
from eipiphany_core.message.exchange import Exchange
from wodpy import wod
import logging

from autoqc_pipeline.model.test_message import TestMessage

logger = logging.getLogger('autoqc.WodpyProfileProcessor')


class WodpyProfileProcessor(Processor):

  def __init__(self, eip_context, file_controller, geohash_service, *args, **kw):
    super().__init__(*args, **kw)
    self.__test_queue_producer = eip_context.get_endpoint('seda:test-queue')
    self.__file_controller = file_controller
    self.__geohash_service = geohash_service


  def process(self, exchange):
    file_message = exchange.body
    file_path_prefix = file_message.file_path_prefix
    logger.info("wodpy profile splitting start {0}".format(file_path_prefix))
    with open(file_message.wod_file_path, 'r') as fid:
      self.__file_controller.on_new_file(file_path_prefix)
      while True:
        profile = wod.WodProfile(fid)
        uid = profile.uid()
        last = profile.is_last_profile_in_file(fid)
        geohash = self.__geohash_service.get_geohash(profile.longitude(), profile.latitude())
        self.__file_controller.on_new_profile(file_path_prefix, uid, last)
        auto_qc_test_message = TestMessage(file_message.file_path_prefix, profile, last, geohash)
        self.__test_queue_producer.process(Exchange(auto_qc_test_message), None)
        logger.debug("wodpy profile {0}:{1}".format(file_path_prefix, uid))
        if last:
          break
    logger.info("wodpy profile splitting end {0}".format(file_path_prefix))
