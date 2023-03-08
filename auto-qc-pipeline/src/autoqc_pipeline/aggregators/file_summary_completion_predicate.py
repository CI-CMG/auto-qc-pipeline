from eipiphany_core.framework.base.predicate import Predicate


class FileDoneCompletionPredicate(Predicate):

  def matches(self, exchange):
    file_summary = exchange.body
    return file_summary.complete
