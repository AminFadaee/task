from abc import ABC, abstractmethod

from storage.storage import Storage
from tasks import Tasks


class TasksManager(ABC):
    storage: Storage
    _tasks_name: str

    @abstractmethod
    def add_entry(self, entry: str):
        pass

    @abstractmethod
    def edit_entry(self, entry: str, new_entry: str):
        pass

    @property
    def storage_path(self):
        return self.storage.path(self._tasks_name)

    @abstractmethod
    def finish_entry(self, entry: str):
        pass

    @abstractmethod
    def retrieve(self) -> Tasks:
        pass


class ManagerFactory(ABC):
    @staticmethod
    @abstractmethod
    def create(name: str) -> TasksManager:
        pass