from .abstract import StorageFactory
from .io import JsonIO
from .parser import SimpleJsonParser
from .storage import Storage


class SimpleJsonStorageFactory(StorageFactory):
    @staticmethod
    def create(storage_path: str):
        return Storage(SimpleJsonParser(), JsonIO(), storage_path)
