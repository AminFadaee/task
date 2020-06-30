from unittest import TestCase

from click.testing import CliRunner

from cli_client import client
from cli_client import config
from cli_client.client import task, add, edit, finish, list_entries, export, undo, remove
from cli_client.factory import ClientManagerFactory
from manager.abstract import TasksManager
from tasks.errors import UniqueViolationError, ConflictError

storage = {}


class ConcreteTasksManager(TasksManager):
    def delete_entry(self, entry: str) -> str:
        global storage
        if self.name not in storage:
            raise LookupError
        storage[self.name].remove(entry)

    def get_entry_full_name(self, partial_name):
        return partial_name

    def edit_entry(self, entry: str, new_entry: str):
        global storage
        if self.name not in storage:
            raise LookupError
        storage[self.name] = new_entry
        return new_entry

    def __init__(self, name):
        self.name = name

    @property
    def storage_path(self) -> str:
        return '.'

    def add_entry(self, entry: str):
        global storage
        if storage.get(self.name, None) and entry in storage[self.name]:
            raise UniqueViolationError
        storage[self.name] = storage.get(self.name, []) + [entry]

    def finish_entry(self, entry: str):
        global storage
        index = storage[self.name].index(entry)
        storage[self.name][index] = storage[self.name][index] + ' done'

    def undo_entry(self, entry: str) -> str:
        global storage
        index = storage[self.name].index(entry + ' done')
        if storage[self.name][index].endswith(' done'):
            storage[self.name][index] = storage[self.name][index][:-5]

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
            self.assertEqual('task_1', storage['work'][0])

    def test_add_accepts_entry_with_spaces(self):
        runner = CliRunner()
        with runner.isolated_filesystem():
            result = runner.invoke(add, ['work', 'this', 'is', 'an', 'entry', 'with', 'spaces'])
            self.assertEqual(0, result.exit_code)
            self.assertEqual('this is an entry with spaces', storage['work'][0])

    def test_add_correctly_adds_to_an_already_existing_group(self):
        runner = CliRunner()
        with runner.isolated_filesystem():
            result = runner.invoke(add, ['work', 'task 1'])
            self.assertEqual(0, result.exit_code)
            self.assertEqual('task 1', storage['work'][0])
            result = runner.invoke(add, ['work', 'task 2'])
            self.assertEqual(0, result.exit_code)
            self.assertEqual('task 2', storage['work'][1])

    def test_add_prints_error_when_entry_already_exists(self):
        runner = CliRunner()
        with runner.isolated_filesystem():
            result = runner.invoke(add, ['work', 'task 1'])
            self.assertEqual(0, result.exit_code)
            self.assertEqual('task 1', storage['work'][0])
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
            self.assertEqual('task', storage['work'][0])
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
            print(result.output)
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
            msg = config.CONFLICTING_ENTRIES.format(entry='task', group='work')
            self.assertEqual(0, result.exit_code)
            self.assertTrue(msg in result.output)
            self.assertEqual({}, storage)
            ConcreteTasksManager.edit_entry = original_edit_entry

    def test_edit_outputs_correct_success_text(self):
        runner = CliRunner()
        with runner.isolated_filesystem():
            result = runner.invoke(add, ['work', 'task_1'])
            self.assertEqual(0, result.exit_code)
            result = runner.invoke(edit, ['work', 'task_1'], input='task_2')
            self.assertEqual(0, result.exit_code)
            self.assertTrue(
                config.EDIT_SUCCESS.format(group='work', entry='task_1', new_entry='task_2') in result.output)

    def test_edit_accepts_entry_with_spaces(self):
        runner = CliRunner()
        with runner.isolated_filesystem():
            result = runner.invoke(add, ['work', 'this', 'is', 'an', 'entry', 'with', 'spaces'])
            self.assertEqual(0, result.exit_code)
            result = runner.invoke(edit, ['work', 'this', 'is', 'an', 'entry', 'with', 'spaces'], input='new_task')
            self.assertEqual(0, result.exit_code)
            self.assertEqual('new_task', storage['work'])

    def test_remove_helps_outputs_the_help(self):
        runner = CliRunner()
        with runner.isolated_filesystem():
            result = runner.invoke(remove, ['--help'])
            self.assertEqual(0, result.exit_code)
            self.assertTrue(config.REMOVE_HELP in result.output)

    def test_remove_removes_the_task_correctly(self):
        runner = CliRunner()
        with runner.isolated_filesystem():
            result = runner.invoke(add, ['work', 'task 1'])
            self.assertEqual(0, result.exit_code)
            result = runner.invoke(add, ['work', 'task 2'])
            self.assertEqual(0, result.exit_code)
            self.assertEqual('task 1', storage['work'][0])
            self.assertEqual('task 2', storage['work'][1])
            result = runner.invoke(remove, ['work', 'task 2'])
            self.assertEqual(0, result.exit_code)
            self.assertEqual('task 1', storage['work'][0])
            self.assertEqual(1, len(storage['work']))

    def test_remove_prints_error_if_entry_does_not_exists(self):
        runner = CliRunner()
        with runner.isolated_filesystem():
            result = runner.invoke(remove, ['work', 'task'])
            msg = config.FAILED_LOOKUP.format(entry='task', group='work')
            print(result.output)
            self.assertEqual(0, result.exit_code)
            self.assertTrue(msg in result.output)
            self.assertEqual({}, storage)

    def test_remove_prints_error_if_entry_matches_more_than_one_tasks(self):
        runner = CliRunner()
        with runner.isolated_filesystem():
            def patched_remove(*args, **kwargs):
                raise ConflictError

            original_remove_entry = ConcreteTasksManager.delete_entry
            ConcreteTasksManager.delete_entry = patched_remove
            result = runner.invoke(remove, ['work', 'task'])
            msg = config.CONFLICTING_ENTRIES.format(entry='task', group='work')
            self.assertEqual(0, result.exit_code)
            self.assertTrue(msg in result.output)
            self.assertEqual({}, storage)
            ConcreteTasksManager.delete_entry = original_remove_entry

    def test_remove_outputs_correct_success_text(self):
        runner = CliRunner()
        with runner.isolated_filesystem():
            result = runner.invoke(add, ['work', 'task_1'])
            self.assertEqual(0, result.exit_code)
            result = runner.invoke(remove, ['work', 'task_1'])
            self.assertEqual(0, result.exit_code)
            self.assertTrue(config.REMOVE_SUCCESS.format(group='work', entry='task_1') in result.output)

    def test_remove_accepts_entry_with_spaces(self):
        runner = CliRunner()
        with runner.isolated_filesystem():
            result = runner.invoke(add, ['work', 'this', 'is', 'an', 'entry', 'with', 'spaces'])
            self.assertEqual(0, result.exit_code)
            result = runner.invoke(remove, ['work', 'this', 'is', 'an', 'entry', 'with', 'spaces'])
            self.assertEqual(0, result.exit_code)
            self.assertEqual(storage['work'], [])

    def test_list_helps_outputs_the_help(self):
        runner = CliRunner()
        with runner.isolated_filesystem():
            result = runner.invoke(list_entries, ['--help'])
            self.assertEqual(0, result.exit_code)
            self.assertTrue(config.LIST_HELP in result.output)

    def test_list_uses_text_presenter(self):
        class MockTextPresenter:
            def __init__(self, tasks, max_width):
                TestClient.mock_text_presenter_called = True

            def present(self, only_unfinished_tasks=False):
                TestClient.mock_text_presenter_only_unfinished_tasks = only_unfinished_tasks

        original_text_presenter = client.TextPresenter
        client.TextPresenter = MockTextPresenter
        runner = CliRunner()
        with runner.isolated_filesystem():
            runner.invoke(add, ['work', 'task 1'])
            runner.invoke(add, ['work', 'task 2'])
            runner.invoke(list_entries, ['work'])
            self.assertTrue(TestClient.mock_text_presenter_called)
            self.assertFalse(TestClient.mock_text_presenter_only_unfinished_tasks)
            runner.invoke(list_entries, ['work', '-u'])
            self.assertTrue(TestClient.mock_text_presenter_called)
            self.assertTrue(TestClient.mock_text_presenter_only_unfinished_tasks)
        client.TextPresenter = original_text_presenter

    def test_finish_helps_outputs_the_help(self):
        runner = CliRunner()
        with runner.isolated_filesystem():
            result = runner.invoke(finish, ['--help'])
            self.assertEqual(0, result.exit_code)
            self.assertTrue(config.FINISH_HELP in result.output)

    def test_finish_finishes_an_entry(self):
        runner = CliRunner()
        with runner.isolated_filesystem():
            runner.invoke(add, ['work', 'task 1'])
            runner.invoke(add, ['work', 'task 2'])
            runner.invoke(finish, ['work', 'task 1'])
            # in the mock, the word 'done' gets appended to the name once finish_entry is called
            self.assertEqual('task 1 done', storage['work'][0])

    def test_undo_helps_outputs_the_help(self):
        runner = CliRunner()
        with runner.isolated_filesystem():
            result = runner.invoke(undo, ['--help'])
            self.assertEqual(0, result.exit_code)
            print(result.output)
            self.assertTrue(config.UNDO_HELP in result.output)

    def test_undo_undoes_an_entry(self):
        runner = CliRunner()
        with runner.isolated_filesystem():
            runner.invoke(add, ['work', 'task 1'])
            runner.invoke(add, ['work', 'task 2'])
            runner.invoke(finish, ['work', 'task 1'])
            runner.invoke(undo, ['work', 'task 1'])
            self.assertEqual('task 1', storage['work'][0])

    def test_export_helps_outputs_the_help(self):
        runner = CliRunner()
        with runner.isolated_filesystem():
            result = runner.invoke(export, ['--help'])
            self.assertEqual(0, result.exit_code)
            self.assertTrue(config.EXPORT_HELP in result.output)

    def tearDown(self) -> None:
        global storage
        storage = {}
        ClientManagerFactory.create = self.original_factory
