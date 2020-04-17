import os
from abc import ABC, abstractmethod


class Exporter(ABC):
    path: str

    def __init__(self, path: str, file_name: str):
        if not os.path.isdir(path):
            os.makedirs(path)
        self.path = os.path.join(path, f'{file_name}.{self.extension}')

    @abstractmethod
    def export(self, content: str, **kwargs):
        pass

    @property
    @abstractmethod
    def extension(self):
        pass
