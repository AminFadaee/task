import os

from tasks import Tasks
from .abstract import IO, Parser


class Storage:
    def __init__(self, parser: Parser, io: IO, storage_path: str):
        self.parser = parser
        self.io = io
        self.storage_path = storage_path
        self.create_path()

    def create_path(self):
        if not os.path.isdir(self.storage_path):
            os.mkdir(self.storage_path)

    def path(self, tasks_name: str):
        return os.path.join(self.storage_path, tasks_name + self.io.extension)

    def put(self, tasks: Tasks):
        path = os.path.join(self.storage_path, self.io.get_file_name(tasks.name))
        content = self.parser.dump(tasks)
        self.io.save_to(content, path)

    def get(self, tasks_name: str):
        path = os.path.join(self.storage_path, self.io.get_file_name(tasks_name))
        try:
            content = self.io.load_from(path)
        except FileNotFoundError:
            self.put(self.parser.load_empty(tasks_name))
            return self.get(tasks_name)
        return self.parser.load(content)
