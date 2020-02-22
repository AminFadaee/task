import json
import os
from unittest import TestCase

from storage.io import JsonIO, IO


class TestIO(TestCase):
    def setUp(self) -> None:
        class ConcreteIO(IO):
            def load_from(self, path: str):
                pass

            def save_to(self, content, path: str):
                pass

            @property
            def extension(self):
                return '.foo'

        self.io = ConcreteIO()

    def test_io_create_file_name_creates_a_correct_name(self):
        cases = [
            {
                'invalid_name': 'some thing invalid',
                'valid_name': 'some_thing_invalid.foo'
            },
            {
                'invalid_name': 'some thing inv@l!d',
                'valid_name': 'some_thing_inv_l_d.foo'
            },
            {
                'invalid_name': 'in_v@l!d',
                'valid_name': 'in_v_l_d.foo'
            }
        ]
        for case in cases:
            self.assertEqual(case['valid_name'], self.io.get_file_name(case['invalid_name']))


class TestJsonIO(TestCase):
    def test_json_io_correctly_loads_a_json_file(self):
        path = './tmp-read.json'
        file = open(path, 'w')
        file.write('{"foo":"bar"}')
        file.close()
        self.assertEqual({"foo": "bar"}, JsonIO().load_from(path))
        os.remove(path)

    def test_json_io_raise_file_not_found_if_file_not_available(self):
        self.assertRaises(FileNotFoundError, JsonIO().load_from, './something not here!')

    def test_json_io_correctly_saves_to_json_file(self):
        path = './tmp-write.json'
        JsonIO().save_to({"foo": "bar"}, path)
        file = open(path)
        content = file.read()
        self.assertEqual(json.loads(content), {"foo": "bar"})
        file.close()
        os.remove(path)

    def test_json_io_gives_the_correct_extension(self):
        self.assertEqual('.json', JsonIO().extension.lower())
