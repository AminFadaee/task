from abc import ABC, abstractmethod

from tasks import Tasks


class Presenter(ABC):
    def __init__(self, tasks: Tasks):
        self.tasks = tasks

    @abstractmethod
    def present(self, only_unfinished_tasks=False):
        pass
