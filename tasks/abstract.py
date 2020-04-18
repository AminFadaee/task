from abc import ABC, abstractmethod
from typing import List


class Task(ABC):
    def __init__(self, name: str):
        self.name = name
        self.done = False

    def finish(self):
        self.done = True

    def undo(self):
        self.done = False

    def __eq__(self, other):
        return self.name == other.name and self.done == other.done


class Tasks(ABC):
    def __init__(self, name: str):
        self.name = name

    @abstractmethod
    def all(self) -> List[Task]:
        pass

    @property
    @abstractmethod
    def number_of_tasks(self) -> int:
        pass

    @abstractmethod
    def add(self, task_name: str) -> Task:
        pass

    @abstractmethod
    def __getitem__(self, item: str):
        pass

    @abstractmethod
    def __setitem__(self, key: str, value: str):
        pass

    @abstractmethod
    def __eq__(self, other):
        pass

    @abstractmethod
    def has(self, name: str) -> bool:
        pass

    @abstractmethod
    def sort_by_name(self, desc=False) -> None:
        pass

    @abstractmethod
    def sort_by_done_state(self, desc=False) -> None:
        pass
