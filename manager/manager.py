from storage.storage import Storage
from tasks import SimpleTasks
from .abstract import TasksManager


class SimpleTasksManager(TasksManager):
    def __init__(self, name: str, storage: Storage):
        self._tasks_name = name
        self._tasks = None
        self.storage = storage

    def get_entry_full_name(self, partial_name):
        tasks = self.retrieve()
        return tasks[partial_name].name

    def add_entry(self, entry: str) -> str:
        tasks = self.retrieve()
        tasks.add(entry)
        self.storage.put(tasks)
        return tasks[entry].name

    def edit_entry(self, entry: str, new_entry: str) -> str:
        tasks = self.retrieve()
        tasks[entry] = new_entry
        self.storage.put(tasks)
        return new_entry

    def finish_entry(self, entry: str) -> str:
        tasks = self.retrieve()
        if tasks.has(entry):
            tasks[entry].finish()
        else:
            task = tasks.add(entry)
            task.finish()
        self.storage.put(tasks)
        return tasks[entry].name

    def undo_entry(self, entry: str) -> str:
        tasks = self.retrieve()
        if tasks.has(entry):
            tasks[entry].undo()
        else:
            tasks.add(entry)
        self.storage.put(tasks)
        return tasks[entry].name

    def retrieve(self) -> SimpleTasks:
        if self._tasks is None:
            self._tasks = self.storage.get(self._tasks_name)
        return self._tasks
