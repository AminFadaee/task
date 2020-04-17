from typing import List, Set

from .abstract import Task, Tasks
from .errors import UniqueViolationError, ConflictError


class SimpleTasks(Tasks):
    class SimpleTask(Task):
        pass

    def __init__(self, name: str):
        super().__init__(name)
        self._tasks: List[Task] = []
        self._task_names: Set[str] = set()

    def all(self) -> List[Task]:
        return self._tasks

    @property
    def number_of_tasks(self):
        return len(self._tasks)

    def add(self, task_name: str):
        if task_name in self._task_names:
            raise UniqueViolationError(f'Task {task_name} already exists in {self.name}')
        task = self.SimpleTask(task_name)
        self._tasks.append(task)
        self._task_names.add(task_name)
        return task

    def _find_task_index_based_on_full_match_or_prefix_match_on_name(self, task_name):
        matched_indices = []
        for index, task in enumerate(self._tasks):
            if task.name == task_name:
                return index
            elif task.name.startswith(task_name):
                matched_indices.append(index)
        if len(matched_indices) > 1:
            raise ConflictError('More than one tasks matched!')
        if len(matched_indices) == 1:
            return matched_indices[0]
        raise LookupError('Task not found!')

    def __getitem__(self, task_name: str):
        index = self._find_task_index_based_on_full_match_or_prefix_match_on_name(task_name)
        return self._tasks[index]

    def __setitem__(self, task_name, new_name: str):
        index = self._find_task_index_based_on_full_match_or_prefix_match_on_name(task_name)
        self._tasks[index].name = new_name

    def __eq__(self, other):
        other_tasks = other.all()
        if len(other_tasks) != len(self._tasks):
            return False
        for index, other_task in enumerate(other_tasks):
            if other_task != self._tasks[index]:
                return False
        return True

    def has(self, name: str):
        return name in self._task_names

    def sort_by_name(self, desc=False):
        self._sort_by_field('name', desc)

    def sort_by_done_state(self, desc=False):
        self._sort_by_field('done', desc)

    def _sort_by_field(self, field: str, desc: bool):
        self._tasks.sort(key=lambda task: getattr(task, field), reverse=desc)
