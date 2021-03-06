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

import logging
import gevent
import gevent.queue


class Job (object):

    PENDING = 'pending'
    FAILURE = 'failede'
    SUCCESS = 'succedded'

    def __init__(self, result=None):
        self.result = Job.PENDING


class Processor (object):

    logger = logging.getLogger('processor-unknown')

    PROCESS_INTERVAL = 0.5

    def __init__(self, task_queue, return_queue, identifier=None):
        self.task_queue = task_queue
        self.return_queue = return_queue
        if identifier is not None:
            self.identifier = identifier
            self.logger = logging.getLogger('processor-for-%s' % identifier)

        self.idling = False
        self.running = False

    def is_idling(self):
        return self.idling

    def start(self):
        if not hasattr(self, 'exec_loop'):
            self.logger.debug('starting the execution loop')
            self.exec_loop = gevent.spawn(self.run_exec_loop)

    def stop(self):
        if hasattr(self, 'exec_loop'):
            self.logger.debug('stopping the execution loop')
            self.running = False
            if not self.exec_loop.ready():
                self.exec_loop.join()
            del self.exec_loop

    def run_exec_loop(self):
        self.running = True
        while self.running:
            # Block getting the next job.
            self.idling = True
            job = self.task_queue.get()
            self.idling = False
            # Process the new job.
            self.logger.debug('processing job')
            gevent.sleep(Processor.PROCESS_INTERVAL)
            job.result = Job.SUCCESS
            # Return the job, now processed.
            self.logger.debug('putting job in result queue')
            self.return_queue.put(job)


class CPU (object):

    logger = logging.getLogger('cpu')

    BOOT_CPU_DELAY = 0.1
    REMOVE_PROCESSOR_DELAY = 0.2
    ADD_PROCESSOR_DELAY = 0.1
    CREATE_PROCESSOR_DELAY = 0.2
    SUBMIT_DELAY = 0.1

    def __init__(self):
        self.processors = {}
        self.task_queue = gevent.queue.Queue()
        self.return_queue = gevent.queue.Queue()
        gevent.sleep(self.BOOT_CPU_DELAY)

    def remove_processor(self, identifier=None, processor=None):
        if processor is not None:
            identifier = processor.identifier

        if identifier not in self.processors:
            raise ValueError('bad processor identifier: %s' % identifier)

        gevent.sleep(self.REMOVE_PROCESSOR_DELAY)
        self.processors[identifier].stop()
        del self.processors[identifier]

    def remove_all_processors(self):
        for identifier in self.processors:
            self.remove_processor(identifier)

    def add_processor(self, processor):
        identifier = processor.identifier
        if identifier in self.processors:
            raise ValueError('processor for %s already in CPU.' % identifier)
        self.logger.debug('adding processor to CPU')
        self.processors[identifier] = processor
        processor.start()

    def new_processor_for(self, identifier):
        self.logger.debug('creating processor for %s' % identifier)
        gevent.sleep(self.CREATE_PROCESSOR_DELAY)
        proc = Processor(self.task_queue, self.return_queue,
                         identifier=identifier)
        gevent.sleep(self.ADD_PROCESSOR_DELAY)
        self.add_processor(proc)

    def submit(self, job):
        gevent.sleep(self.SUBMIT_DELAY)
        self.logger.debug('putting job on task queue')
        self.task_queue.put(job)


__cpu = None


# Create the CPU instance on demand to produce the delay.
def get_cpu():
    global __cpu
    if __cpu is None:
        __cpu = CPU()
    return __cpu
