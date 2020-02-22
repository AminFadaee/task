import os
from unittest import TestCase

from storage import SimpleJsonStorageFactory
from storage.abstract import Parser
from storage.io import IO, JsonIO
from storage.parser import SimpleJsonParser
from storage.storage import Storage
from tasks import Tasks, SimpleTasks


class StubIO(IO):
    def __init__(self):
        self.file = {}

    def load_from(self, path: str):
        return self.file[path]

    def save_to(self, content, path: str):
        self.file[path] = content

    @property
    def extension(self):
        return '.stub'


class StubParser(Parser):
    def load_empty(self, name) -> Tasks:
        return SimpleTasks(name)

    def load(self, content) -> Tasks:
        tasks = SimpleTasks('stub')
        tasks.add('Stub Job 1')
        tasks.add('Stub Job 2')
        return tasks

    def dump(self, tasks: Tasks):
        return 'Stub Job 1'


class TestStorage(TestCase):
    def test_storage_put_adds_task_to_storage(self):
        storage = Storage(StubParser(), StubIO(), '.')
        storage.put(SimpleTasks('name'))
        self.assertEqual('Stub Job 1', storage.io.file['./name.stub'])

    def test_storage_create_path_creates_the_path_if_it_does_not_exists(self):
        Storage(StubParser(), StubIO(), './foo')
        self.assertTrue(os.path.isdir('./foo'))
        os.rmdir('./foo')

    def test_storage_create_path_does_not_raise_exception_if_path_already_exists(self):
        Storage(StubParser(), StubIO(), './bar')
        self.assertTrue(os.path.isdir('./bar'))
        Storage(StubParser(), StubIO(), './bar')
        self.assertTrue(os.path.isdir('./bar'))
        os.rmdir('./bar')

    def test_storage_get_fetches_from_storage_correctly(self):
        storage = Storage(StubParser(), StubIO(), '.')
        storage.io.file['./name.stub'] = 'foo'
        tasks = storage.get('name')
        self.assertTrue(isinstance(tasks, Tasks))
        self.assertEqual('Stub Job 1', tasks.all()[0].name)
        self.assertEqual('Stub Job 2', tasks.all()[1].name)

    def test_storage_path_gives_the_correct_path_to_the_storage_of_a_given_tasks(self):
        storage = Storage(StubParser(), StubIO(), '.')
        self.assertEqual('./foo.stub', storage.path('foo'))


class TestSimpleJsonStorageFactory(TestCase):
    def test_json_storage_factory_uses_json_io_and_json_parser_to_create_a_storage(self):
        storage = SimpleJsonStorageFactory.create('.')
        self.assertTrue(isinstance(storage, Storage))
        self.assertTrue(isinstance(storage.io, IO))
        self.assertTrue(isinstance(storage.parser, Parser))
        self.assertTrue(isinstance(storage.io, JsonIO))
        self.assertTrue(isinstance(storage.parser, SimpleJsonParser))
