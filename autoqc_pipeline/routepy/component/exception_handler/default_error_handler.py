import logging

from autoqc_pipeline.routepy.framework.error_handler import ErrorHandler

logger = logging.getLogger(__name__)


class DefaultErrorHandler(ErrorHandler):

  def handle_exception(self, exchange):
    exception = exchange.get_header(ErrorHandler.EXCEPTION_CAUGHT)
    logger.error("Exception in route", exc_info=exception)

