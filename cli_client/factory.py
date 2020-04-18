import click

from manager.abstract import ManagerFactory
from manager.manager import SimpleTasksManager
from storage import SimpleJsonStorageFactory


class ClientManagerFactory(ManagerFactory):
    @staticmethod
    def create(name: str):
        storage_path = click.get_app_dir('tasks')
        return SimpleTasksManager(name, SimpleJsonStorageFactory().create(storage_path))
