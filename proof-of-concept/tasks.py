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


class EndingTask:
    """Represent an class of objects encapsulating a task which will
    finish... at some point. En example of this task can be a long running
    one-off task which is sent to the background to avoid blocking the system
    (like sending an email).

    Takes advantage of testing convention: defines attribute 'greenlet' at
    __init__, which will hold the one greenlet with the task to wait for.

    The result of the task is stored in an instance attribute by the greenlet.
    """

    SLEEP_COUNTER = 5
    SLEEP_INTERVAL = 0.1

    def __init__(self):
        # keep a per-instance counter for the resource used.
        self.sleep_counter = self.SLEEP_COUNTER

        # Take this name from __init__ for testing purposes (ugh!)
        self.greenlet = None

    def start(self):
        "Start the task in a fresh greenlet, wrapped by this instance"
        # Reference the task with the known 'greenlet' symbol.
        self.greenlet = gevent.spawn(self.run_task)

    def run_task(self, *args, **kwargs):
        "The task this object encapsulates"
        # This task will complete once self.sleep_counter is zero.
        while self.sleep_counter > 0:
            gevent.sleep(self.SLEEP_INTERVAL)
            self.sleep_counter = self.sleep_counter - 1
        self.result = 'done!'


class PersistentTask:
    """Represent an class of objects encapsulating a task which may run
    forever. This task is guaranteed to have "down times" during which testing
    is allowed. En example of this kind of tasks is stealing work from a queu,
    where blocking is common.

    Takes advange of the testing convention: use a method named is_idling()
    which takes no arguments to mark when the task is idling and available for
    testing.
    """

    DOWN_TIME_INTERVAL = 1
    UP_TIME_INTERVAL = 0.1

    def __init__(self):
        # Use this flag to expose whether the task is in a "down time" or not
        self.waiting_for_resource = False

    def is_idling(self):
        return self.waiting_for_resource

    def run_forever(self, *args, **kwargs):
        while True:
            # Block on a resource or queue, etc.
            self.waiting_for_resource = True
            gevent.sleep(self.DOWN_TIME_INTERVAL)
            self.waiting_for_resource = False
            gevent.sleep((self.UP_TIME_INTERVAL))

    def start(self):
        gevent.spawn(self.run_forever)
