from eipiphany_core.framework.base.processor import Processor

from ..model.file_message import FileMessage


class FileMessageProcessor(Processor):

  def process(self, exchange):
    gzip_file_path = exchange.body
    exchange.body = FileMessage().set_gzip_file_path(gzip_file_path)
