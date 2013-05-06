import gevent
import unittest


class SyncTestCase (unittest.TestCase):

    def when(self, prop, *args, **kwargs):
        condition = prop
        # if hasattr(prop, 'is_idling') and callable(prop.is_idling):
        #     condition = prop.is_idling

        if not callable(condition):
            raise ValueError('first argmument must be... nicer')

        while not condition(*args, **kwargs):
            gevent.sleep()

        return self

    def after(self, action, *args, **kwargs):
        if not callable(action):
            raise ValueError('first argmument must be... nicer')

        gevent.spawn(action, *args, **kwargs).join()

        return self
