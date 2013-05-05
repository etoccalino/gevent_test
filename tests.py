import synctest
import target
import complex_target


def ending_task_is_done(self):
    return self.greenlet.ready()

target.EndingTask.is_done = ending_task_is_done


class TaskTestCase (synctest.SyncTestCase):

    def test_ending_task(so):
        task = target.EndingTask()
        task.start()
        so.when(task.is_done).assertEqual(task.result, 'done!')

    def test_persistent_task(so):
        task = target.PersistentTask()
        task.start()
        so.when(task.is_idling).assertTrue(task.waiting_for_resource)


class ComplexTestCase (synctest.SyncTestCase):

    def test_task(so):
        cpu = complex_target.get_cpu()
        cpu.remove_all_processors()
        cpu.new_processor_for('some-robot')

        processor = cpu.processors['some-robot']
        job = complex_target.Job()

        (so.after(cpu.submit, job).when(processor.is_idling)
         .assertEqual(job.result, complex_target.Job.SUCCESS))
