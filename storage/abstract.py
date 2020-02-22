import string
from abc import ABC, abstractmethod

from tasks import Tasks


class IO(ABC):
    @abstractmethod
    def load_from(self, path: str):
        pass

    @abstractmethod
    def save_to(self, content, path: str):
        pass

    @property
    @abstractmethod
    def extension(self):
        pass

    def get_file_name(self, name: str):
        valid_characters = string.ascii_letters + string.digits
        file_name = ''.join(
            character if character in valid_characters else '_'
            for character in name
        ) + self.extension
        return file_name


class Parser(ABC):
    @abstractmethod
    def load_empty(self, name) -> Tasks:
        pass

    @abstractmethod
    def load(self, content) -> Tasks:
        pass

    @abstractmethod
    def dump(self, tasks: Tasks):
        pass


class StorageFactory(ABC):
    @staticmethod
    @abstractmethod
    def create(storage_path: str):
        pass
