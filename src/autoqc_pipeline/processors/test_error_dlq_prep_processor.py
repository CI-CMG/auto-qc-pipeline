import logging

from eipiphany_core.framework.base.error_handler import ErrorHandler
from eipiphany_core.framework.base.processor import Processor

logger = logging.getLogger(__name__)

class TestErrorDlqPrepProcessor(Processor):

  DEFAULT_ERROR = "An undetermined error occurred during processing"

  def process(self, exchange):
    cause = exchange.get_header(ErrorHandler.EXCEPTION_CAUGHT)
    detail = exchange.get_header(ErrorHandler.EXCEPTION_CAUGHT_DETAIL)
    logger.error("Exception in route (" + cause + ") " + detail)


    error_message = str(cause)
    if not error_message:
      error_message = detail
    if not error_message:
      error_message = TestErrorDlqPrepProcessor.DEFAULT_ERROR

    test_message = exchange.body
    test_message.profile_test_result.exception = error_message
