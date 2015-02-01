from django.db.models.query import EmptyQuerySet

class FakeQuerySet(EmptyQuerySet):
    """
    This represents a QuerySet which behaves like one, but isn't. It allows
    one to convert a list of items to a query set.
    """

    def __init__(self, model=None, query=None, using=None, items=[]):
        super(FakeQuerySet, self).__init__(model, query, using)
        self._result_cache = items

    def count(self):
        return len(self)