from unittest import TestCase

from storage.parser import SimpleJsonParser
from tasks import SimpleTasks


class TestSimpleJsonParser(TestCase):
    def test_json_parser_loads_empty_loads_an_empty_simple_tasks(self):
        tasks = SimpleJsonParser().load_empty('work')
        self.assertTrue(isinstance(tasks, SimpleTasks))
        self.assertEqual('work', tasks.name)
        self.assertEqual([], tasks.all())

    def test_json_parser_dump_correctly_creates_a_json_from_tasks(self):
        tasks = SimpleTasks('work')
        tasks.add('Job 1')
        tasks.add('Job 2')
        tasks.add('Job 3')
        tasks['Job 1'].finish()
        tasks['Job 3'].finish()
        expected = {
            "group": "work",
            "tasks": [
                {
                    "name": "Job 1",
                    "done": True
                },
                {
                    "name": "Job 2",
                    "done": False
                },
                {
                    "name": "Job 3",
                    "done": True
                }
            ]
        }
        self.assertEqual(expected, SimpleJsonParser().dump(tasks))

    def test_json_parser_load_creates_tasks_correctly(self):
        content = {
            "group": "work",
            "tasks": [
                {
                    "name": "Job 1",
                    "done": True
                },
                {
                    "name": "Job 2",
                    "done": False
                },
                {
                    "name": "Job 3",
                    "done": True
                }
            ]
        }
        tasks = SimpleTasks('work')
        tasks.add('Job 1')
        tasks.add('Job 2')
        tasks.add('Job 3')
        tasks['Job 1'].finish()
        tasks['Job 3'].finish()
        self.assertEqual(tasks, SimpleJsonParser().load(content))
