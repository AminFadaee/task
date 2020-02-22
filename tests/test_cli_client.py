from unittest import TestCase

from click.testing import CliRunner

from cli_client import config
from cli_client.client import task, group, add, edit, finish, list_entries, export
from cli_client.factory import ClientManagerFactory
from manager.abstract import TasksManager
from tasks.errors import UniqueViolationError, ConflictError

storage = {}


class ConcreteTasksManager(TasksManager):
    def edit_entry(self, entry: str, new_entry: str):
        global storage
        if self.name not in storage:
            raise LookupError
        storage[self.name] = new_entry

    def __init__(self, name):
        self.name = name

    @property
    def storage_path(self) -> str:
        return '.'

    def add_entry(self, entry: str):
        global storage
        if storage.get(self.name) == entry:
            raise UniqueViolationError
        storage[self.name] = entry

    def finish_entry(self, entry: str):
        pass

    def retrieve(self):
        global storage
        storage['retrieve_called'] = True


class TestClientManagerFactory(TestCase):
    def test_client_manager_factory_returns_a_valid_manager(self):
        self.assertTrue(isinstance(ClientManagerFactory.create('foo'), TasksManager))


class TestClient(TestCase):
    def setUp(self) -> None:
        def mock_create(name):
            return ConcreteTasksManager(name)

        self.original_factory = ClientManagerFactory.create
        ClientManagerFactory.create = mock_create

    def test_task_helps_outputs_the_help(self):
        runner = CliRunner()
        with runner.isolated_filesystem():
            result = runner.invoke(task, ['--help'])
            self.assertEqual(0, result.exit_code)
            self.assertTrue(config.TASK_HELP in result.output)

    def test_add_helps_outputs_the_help(self):
        runner = CliRunner()
        with runner.isolated_filesystem():
            result = runner.invoke(add, ['--help'])
            self.assertEqual(0, result.exit_code)
            self.assertTrue(config.ADD_HELP in result.output)

    def test_add_outputs_correct_success_text(self):
        runner = CliRunner()
        with runner.isolated_filesystem():
            result = runner.invoke(add, ['work', 'task_1'])
            self.assertEqual(0, result.exit_code)
            self.assertTrue(config.ADD_SUCCESS.format(group='work', entry='task_1') in result.output)

    def test_add_creates_group_if_not_existing(self):
        runner = CliRunner()
        with runner.isolated_filesystem():
            result = runner.invoke(add, ['work', 'task_1'])
            self.assertEqual(0, result.exit_code)
            self.assertEqual('task_1', storage['work'])

    def test_add_accepts_entry_with_spaces(self):
        runner = CliRunner()
        with runner.isolated_filesystem():
            result = runner.invoke(add, ['work', 'this', 'is', 'an', 'entry', 'with', 'spaces'])
            self.assertEqual(0, result.exit_code)
            self.assertEqual('this is an entry with spaces', storage['work'])

    def test_add_correctly_adds_to_an_already_existing_group(self):
        runner = CliRunner()
        with runner.isolated_filesystem():
            result = runner.invoke(add, ['work', 'task 1'])
            self.assertEqual(0, result.exit_code)
            self.assertEqual('task 1', storage['work'])
            result = runner.invoke(add, ['work', 'task 2'])
            self.assertEqual(0, result.exit_code)
            self.assertEqual('task 2', storage['work'])

    def test_add_prints_error_when_entry_already_exists(self):
        runner = CliRunner()
        with runner.isolated_filesystem():
            result = runner.invoke(add, ['work', 'task 1'])
            self.assertEqual(0, result.exit_code)
            self.assertEqual('task 1', storage['work'])
            result = runner.invoke(add, ['work', 'task 1'])
            self.assertEqual(0, result.exit_code)
            self.assertTrue(config.ADD_FAILED.format(group='work', entry='task 1') in result.output)

    def test_edit_helps_outputs_the_help(self):
        runner = CliRunner()
        with runner.isolated_filesystem():
            result = runner.invoke(edit, ['--help'])
            self.assertEqual(0, result.exit_code)
            self.assertTrue(config.EDIT_HELP in result.output)

    def test_edit_changes_the_entry_name_correctly(self):
        runner = CliRunner()
        with runner.isolated_filesystem():
            result = runner.invoke(add, ['work', 'task'])
            self.assertEqual(0, result.exit_code)
            self.assertEqual('task', storage['work'])
            result = runner.invoke(edit, ['work', 'task'], input='another task')
            msg = config.EDIT_SUCCESS.format(entry='task', new_entry='another task', group='work')
            self.assertEqual(0, result.exit_code)
            self.assertTrue(msg in result.output)
            self.assertEqual('another task', storage['work'])

    def test_edit_prints_error_if_entry_does_not_exists(self):
        runner = CliRunner()
        with runner.isolated_filesystem():
            result = runner.invoke(edit, ['work', 'task'], input='another task')
            msg = config.FAILED_LOOKUP.format(entry='task', group='work')
            self.assertEqual(0, result.exit_code)
            self.assertTrue(msg in result.output)
            self.assertEqual({}, storage)

    def test_edit_prints_error_if_entry_matches_more_than_one_tasks(self):
        runner = CliRunner()
        with runner.isolated_filesystem():
            def patched_edit(*args, **kwargs):
                raise ConflictError

            original_edit_entry = ConcreteTasksManager.edit_entry
            ConcreteTasksManager.edit_entry = patched_edit
            result = runner.invoke(edit, ['work', 'task'], input='another task')
            msg = config.EDIT_FAILED_CONFLICT.format(entry='task', group='work')
            self.assertEqual(0, result.exit_code)
            self.assertTrue(msg in result.output)
            self.assertEqual({}, storage)
            ConcreteTasksManager.edit_entry = original_edit_entry

    def test_finish_helps_outputs_the_help(self):
        runner = CliRunner()
        with runner.isolated_filesystem():
            result = runner.invoke(finish, ['--help'])
            self.assertEqual(0, result.exit_code)
            self.assertTrue(config.FINISH_HELP in result.output)

    def test_edit_outputs_correct_success_text(self):
        runner = CliRunner()
        with runner.isolated_filesystem():
            result = runner.invoke(add, ['work', 'task_1'])
            self.assertEqual(0, result.exit_code)
            self.assertTrue(config.ADD_SUCCESS.format(group='work', entry='task_1') in result.output)

    def test_edit_creates_group_if_not_existing(self):
        runner = CliRunner()
        with runner.isolated_filesystem():
            result = runner.invoke(add, ['work', 'task_1'])
            self.assertEqual(0, result.exit_code)
            self.assertEqual('task_1', storage['work'])

    def test_edit_accepts_entry_with_spaces(self):
        runner = CliRunner()
        with runner.isolated_filesystem():
            result = runner.invoke(add, ['work', 'this', 'is', 'an', 'entry', 'with', 'spaces'])
            self.assertEqual(0, result.exit_code)
            self.assertEqual('this is an entry with spaces', storage['work'])

    def test_edit_correctly_adds_to_an_already_existing_group(self):
        runner = CliRunner()
        with runner.isolated_filesystem():
            result = runner.invoke(add, ['work', 'task 1'])
            self.assertEqual(0, result.exit_code)
            self.assertEqual('task 1', storage['work'])
            result = runner.invoke(add, ['work', 'task 2'])
            self.assertEqual(0, result.exit_code)
            self.assertEqual('task 2', storage['work'])

    def test_edit_does_not_print_error_when_entry_already_exists(self):
        runner = CliRunner()
        with runner.isolated_filesystem():
            result = runner.invoke(add, ['work', 'task 1'])
            self.assertEqual(0, result.exit_code)
            self.assertEqual('task 1', storage['work'])
            result = runner.invoke(add, ['work', 'task 1'])
            self.assertEqual(0, result.exit_code)
            self.assertTrue(config.ADD_FAILED.format(group='work', entry='task 1') in result.output)

    def test_group_helps_outputs_the_help(self):
        runner = CliRunner()
        with runner.isolated_filesystem():
            result = runner.invoke(group, ['--help'])
            self.assertEqual(0, result.exit_code)
            self.assertTrue(config.GROUP_HELP in result.output)

    def test_list_helps_outputs_the_help(self):
        runner = CliRunner()
        with runner.isolated_filesystem():
            result = runner.invoke(list_entries, ['--help'])
            self.assertEqual(0, result.exit_code)
            self.assertTrue(config.LIST_HELP in result.output)

    def test_export_helps_outputs_the_help(self):
        runner = CliRunner()
        with runner.isolated_filesystem():
            result = runner.invoke(export, ['--help'])
            self.assertEqual(0, result.exit_code)
            self.assertTrue(config.EXPORT_HELP in result.output)

    def test_group_adds_a_tasks_correctly(self):
        runner = CliRunner()
        with runner.isolated_filesystem():
            result = runner.invoke(group, ['foo'])
            self.assertEqual(0, result.exit_code)
            self.assertTrue(storage['retrieve_called'])

    def tearDown(self) -> None:
        global storage
        storage = {}
        ClientManagerFactory.create = self.original_factory
