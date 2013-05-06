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
