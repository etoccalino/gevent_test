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

import gevent_test
import tasks
import related


def ending_task_is_done(self):
    return self.greenlet.ready()

tasks.EndingTask.is_done = ending_task_is_done


class TaskTestCase (gevent_test.SyncTestCase):

    def test_ending_task(so):
        task = tasks.EndingTask()
        task.start()
        so.when(task.is_done).assertEqual(task.result, 'done!')

    def test_persistent_task(so):
        task = tasks.PersistentTask()
        task.start()
        so.when(task.is_idling).assertTrue(task.waiting_for_resource)


class RelatedTestCase (gevent_test.SyncTestCase):

    def test_task(so):
        cpu = related.get_cpu()
        cpu.remove_all_processors()
        cpu.new_processor_for('some-robot')

        processor = cpu.processors['some-robot']
        job = related.Job()

        (so.after(cpu.submit, job).when(processor.is_idling)
         .assertEqual(job.result, related.Job.SUCCESS))
