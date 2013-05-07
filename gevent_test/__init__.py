# Copyright (c) 2013, Elvio Toccalino
# All rights reserved.

# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#     * Redistributions of source code must retain the above copyright
#       notice, this list of conditions and the following disclaimer.
#     * Redistributions in binary form must reproduce the above copyright
#       notice, this list of conditions and the following disclaimer in the
#       documentation and/or other materials provided with the distribution.
#     * Neither the name of the <organization> nor the
#       names of its contributors may be used to endorse or promote products
#       derived from this software without specific prior written permission.

# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
# ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL <COPYRIGHT HOLDER> BE LIABLE FOR ANY
# DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
# (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
# ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
# SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

import gevent
import unittest


def _when(self, condition, *args, **kwargs):
    """Wait until the condition is met before proceeding.

    Returns the test instance, to allow chaining an assert method.

    The `condition` must be a callable, returning truthy-falsy.
    """
    if not callable(condition):
        raise ValueError('first argmument must be a callable proposition')

    gevent.sleep()
    while not condition(*args, **kwargs):
        gevent.sleep()

    return self


def _after(self, action, *args, **kwargs):
    """Wait until the action finishes before proceeding.

    Returns the test instance, to allow chaining an assert method.

    The `condition` must be a callable, returning truthy-falsy.
    """
    if not callable(action):
        raise ValueError('first argmument must be a callable')

    gevent.spawn(action, *args, **kwargs).join()

    return self


def _yield(self):
    gevent.sleep()


class SyncMixin (object):

    when = _when

    after = _after

    yield_control = _yield


class SyncTestCase (unittest.TestCase, SyncMixin):
    pass


def patch(cls):
    cls.when = _when
    cls.after = _after
    cls.yield_control = _yield
    return cls
