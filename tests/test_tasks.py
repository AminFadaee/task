from unittest import TestCase

from tasks import SimpleTasks, Task
from tasks.errors import UniqueViolationError


class TestSimpleTasks(TestCase):
    def test_tasks_is_initialized_with_a_name(self):
        self.assertTrue(SimpleTasks('work'))

    def test_tasks_is_empty_when_initialized(self):
        tasks = SimpleTasks('work')
        self.assertEqual(0, tasks.number_of_tasks)

    def test_tasks_add_gets_a_name_and_adds_a_task(self):
        tasks = SimpleTasks('work')
        tasks.add('tasks 1')
        self.assertEqual(1, tasks.number_of_tasks)

    def test_tasks_number_of_tasks_correctly_computes_number_of_tasks(self):
        tasks = SimpleTasks('work')
        self.assertEqual(0, tasks.number_of_tasks)
        for i in range(10):
            tasks.add(f'tasks {i}')
            self.assertEqual(1 + i, tasks.number_of_tasks)

    def test_tasks_all_returns_all_the_tasks_in_tasks(self):
        tasks = SimpleTasks('work')
        tasks.add('tasks 1')
        tasks.add('tasks 2')
        task_list = tasks.all()
        self.assertTrue(isinstance(task_list[0], Task))
        self.assertTrue(isinstance(task_list[1], Task))
        self.assertEqual(task_list[0].name, 'tasks 1')
        self.assertEqual(task_list[1].name, 'tasks 2')

    def test_tasks_all_is_empty_when_initialized(self):
        tasks = SimpleTasks('work')
        self.assertEqual(0, len(tasks.all()))

    def test_tasks_add_raises_unique_violation_error_when_duplicate_task_is_added(self):
        tasks = SimpleTasks('work')
        tasks.add('tasks 1')
        self.assertRaises(UniqueViolationError, tasks.add, 'tasks 1')

    def test_tasks_getitem_accesses_a_task_in_tasks(self):
        tasks = SimpleTasks('work')
        tasks.add('tasks 1')
        tasks.add('tasks 2')
        tasks.add('tasks 3')
        self.assertTrue(isinstance(tasks['tasks 1'], Task))
        self.assertEqual('tasks 2', tasks['tasks 2'].name)
        self.assertRaises(LookupError, tasks.__getitem__, 'tasks 5')
        tasks['tasks 1'].finish()
        self.assertTrue(tasks['tasks 1'].done)

    def test_sort_by_name_sorts_correctly(self):
        tasks = SimpleTasks('work')
        tasks.add('tasks 2')
        tasks.add('tasks 1')
        tasks.add('tasks 3')
        self.assertEqual(['tasks 2', 'tasks 1', 'tasks 3'], list(map(lambda i: i.name, tasks.all())))
        tasks.sort_by_name()
        self.assertEqual(['tasks 1', 'tasks 2', 'tasks 3'], list(map(lambda i: i.name, tasks.all())))
        tasks.sort_by_name(desc=True)
        self.assertEqual(['tasks 3', 'tasks 2', 'tasks 1'], list(map(lambda i: i.name, tasks.all())))

    def test_sort_by_done_state_sorts_correctly(self):
        tasks = SimpleTasks('work')
        tasks.add('tasks 1')
        tasks.add('tasks 2')
        tasks.add('tasks 3')
        tasks.add('tasks 4')
        tasks['tasks 1'].finish()
        tasks['tasks 4'].finish()
        self.assertEqual(['tasks 1', 'tasks 2', 'tasks 3', 'tasks 4'], list(map(lambda i: i.name, tasks.all())))
        tasks.sort_by_done_state()
        self.assertEqual(['tasks 2', 'tasks 3', 'tasks 1', 'tasks 4'], list(map(lambda i: i.name, tasks.all())))
        tasks.sort_by_done_state(desc=True)
        self.assertEqual(['tasks 1', 'tasks 4', 'tasks 2', 'tasks 3'], list(map(lambda i: i.name, tasks.all())))

    def test_equality_works_correctly_for_tasks(self):
        tasks1 = SimpleTasks('work')
        tasks1.add('tasks 1')
        tasks1.add('tasks 2')
        tasks2 = SimpleTasks('work')
        tasks2.add('tasks 1')
        tasks2.add('tasks 2')
        self.assertEqual(tasks1, tasks2)
        tasks3 = SimpleTasks('foobar')
        self.assertNotEqual(tasks1, tasks3)
        tasks2['tasks 1'].finish()
        self.assertNotEqual(tasks1, tasks2)

    def test_has_looks_up_correctly(self):
        tasks = SimpleTasks('work')
        tasks.add('tasks 1')
        tasks.add('tasks 2')
        self.assertFalse(tasks.has('tasks 3'))
        self.assertTrue(tasks.has('tasks 2'))
        self.assertTrue(tasks.has('tasks 1'))
