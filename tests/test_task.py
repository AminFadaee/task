from unittest import TestCase

from tasks import Task


class TestTask(TestCase):
    def setUp(self) -> None:
        class ConcreteTask(Task):
            pass

        self.Task = ConcreteTask

    def test_task_initializes_with_a_name(self):
        self.assertTrue(self.Task('my tasks'))

    def test_task_state_is_unfinished_when_initialized(self):
        task = self.Task('my tasks')
        self.assertEqual(False, task.done)

    def test_task_state_is_finished_when_finish_is_called(self):
        task = self.Task('my tasks')
        task.finish()
        self.assertEqual(True, task.done)

    def test_task_state_is_unfinished_when_undo_is_called(self):
        task = self.Task('my tasks')
        task.finish()
        self.assertEqual(True, task.done)
        task.undo()
        self.assertEqual(False, task.done)

    def test_task_equality_works_correctly(self):
        task1 = self.Task('my tasks')
        task2 = self.Task('my tasks')
        self.assertEqual(task1, task2)
        task2.finish()
        self.assertNotEqual(task1, task2)
