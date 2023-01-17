from autoqc_pipeline.model.auto_qc_message import AutoQcMessage
from autoqc_pipeline.routepy.framework.processor import Processor


class MessagePrepProcessor(Processor):

  def process(self, exchange):
    exchange.set_body(AutoQcMessage().set_gzip_file_path(exchange.get_body()))
