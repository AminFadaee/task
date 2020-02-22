from storage.storage import Storage
from tasks import SimpleTasks
from .abstract import TasksManager


class SimpleTasksManager(TasksManager):
    def __init__(self, name: str, storage: Storage):
        self._tasks_name = name
        self._tasks = None
        self.storage = storage

    def add_entry(self, entry: str):
        tasks = self.retrieve()
        tasks.add(entry)
        self.storage.put(tasks)

    def edit_entry(self, entry: str, new_entry: str):
        tasks = self.retrieve()
        tasks[entry] = new_entry
        self.storage.put(tasks)

    def finish_entry(self, entry: str):
        tasks = self.retrieve()
        if tasks.has(entry):
            tasks[entry].finish()
        else:
            task = tasks.add(entry)
            task.finish()
        self.storage.put(tasks)

    def retrieve(self) -> SimpleTasks:
        if self._tasks is None:
            self._tasks = self.storage.get(self._tasks_name)
        return self._tasks
