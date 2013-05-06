import gevent
import unittest


class SyncTestCase (unittest.TestCase):

    def when(self, condition, *args, **kwargs):
        """Wait until the condition is met before proceeding.

        Returns the test instance, to allow chaining an assert method.

        The `condition` must be a callable, returning truthy-falsy.
        """
        if not callable(condition):
            raise ValueError('first argmument must be a callable proposition')

        while not condition(*args, **kwargs):
            gevent.sleep()

        return self

    def after(self, action, *args, **kwargs):
        """Wait until the action finishes before proceeding.

        Returns the test instance, to allow chaining an assert method.

        The `condition` must be a callable, returning truthy-falsy.
        """
        if not callable(action):
            raise ValueError('first argmument must be a callable')

        gevent.spawn(action, *args, **kwargs).join()

        return self
