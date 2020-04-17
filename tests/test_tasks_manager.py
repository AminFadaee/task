from unittest import TestCase

from manager.manager import SimpleTasksManager
from storage.io import IO
from storage.parser import SimpleJsonParser
from storage.storage import Storage
from tasks import SimpleTasks
from tasks.errors import UniqueViolationError

file = {}


class MockIO(IO):
    def load_from(self, path: str):
        if path not in file:
            raise FileNotFoundError
        return file[path]

    def save_to(self, content, path: str):
        file[path] = content

    @property
    def extension(self):
        return '.foo'


class TestTasksManager(TestCase):
    def setUp(self) -> None:
        self.storage = Storage(SimpleJsonParser(), MockIO(), '.')

    def test_tasks_manager_initializes_with_a_name_and_a_storage(self):
        self.assertTrue(SimpleTasksManager('work', self.storage))

    def test_tasks_manager_add_entry_creates_the_appropriate_file_if_not_existing_already(self):
        tasks_manager = SimpleTasksManager('work', self.storage)
        tasks_manager.add_entry(entry='job 1')
        self.assertTrue('./work.foo' in file)

    def test_tasks_manager_finish_entry_creates_and_finishes_task_if_not_existing_already(self):
        tasks_manager = SimpleTasksManager('work', self.storage)
        tasks_manager.finish_entry(entry='job 1')
        self.assertTrue('./work.foo' in file)
        self.assertEqual(file['./work.foo'], {'group': 'work', 'tasks': [{'done': True, 'name': 'job 1'}]})

    def test_tasks_manager_finish_makes_the_entry_done_if_it_already_existing(self):
        tasks_manager = SimpleTasksManager('work', self.storage)
        tasks_manager.add_entry('job 1')
        tasks_manager.finish_entry(entry='job 1')
        self.assertEqual(file['./work.foo'], {'group': 'work', 'tasks': [{'done': True, 'name': 'job 1'}]})

    def test_tasks_manager_retrieve_returns_a_tasks(self):
        tasks_manager = SimpleTasksManager('work', self.storage)
        tasks = tasks_manager.retrieve()
        self.assertTrue(isinstance(tasks, SimpleTasks))

    def test_tasks_manager_storage_path_use_storage_path_method_to_give_the_path(self):
        tasks_manager = SimpleTasksManager('work', self.storage)
        self.assertEqual('./work.foo', tasks_manager.storage_path)

    def test_manager_raises_error_when_task_already_exists(self):
        tasks_manager = SimpleTasksManager('work', self.storage)
        tasks_manager.add_entry('job 1')
        self.assertRaises(UniqueViolationError, tasks_manager.add_entry, 'job 1')

    def test_manager_edit_renames_task_correctly(self):
        tasks_manager = SimpleTasksManager('work', self.storage)
        tasks_manager.add_entry('job 1')
        tasks_manager.edit_entry('job 1', 'one job')
        self.assertEqual(1, len(file['./work.foo']['tasks']))
        self.assertEqual('one job', file['./work.foo']['tasks'][0]['name'])

    def test_manager_edit_renames_task_correctly_given_partial_match_of_task_name_based_on_name_prefix(self):
        tasks_manager = SimpleTasksManager('work', self.storage)
        tasks_manager.add_entry('one job')
        tasks_manager.edit_entry('one', 'yet another job')
        self.assertEqual(1, len(file['./work.foo']['tasks']))
        self.assertEqual('yet another job', file['./work.foo']['tasks'][0]['name'])

    def test_manager_get_full_name_get_the_complete_name_of_the_entry_correctly(self):
        tasks_manager = SimpleTasksManager('work', self.storage)
        tasks_manager.add_entry('one job')
        tasks_manager.add_entry('two job')
        tasks_manager.add_entry('three job')
        self.assertEqual('one job', tasks_manager.get_entry_full_name('one'))

    def tearDown(self) -> None:
        global file
        file = {}
