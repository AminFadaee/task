from presenter.abstract import Presenter
from tasks import Tasks, Task


class TextPresenter(Presenter):
    def __init__(self, tasks: Tasks, max_width):
        super().__init__(tasks)
        self.output = ''
        self.max_width = max_width
        self._width = None

    def present_task(self, task: Task):
        name = task.name
        chunks = []
        while name:
            chunks.append(' ' * len('[ ] ') + name[:self.max_width - 4].strip())
            name = name[self.max_width - 4:]
        status = f"[{[' ', 'x'][task.done]}] "
        chunks[0] = status + chunks[0][4:]
        return '\n'.join(chunks)

    def present(self, only_unfinished_tasks=False):
        output = f'{self.title}\n{self.line}'
        for task in self.tasks.all():
            if only_unfinished_tasks and task.done:
                continue
            output = f'{output}\n{self.present_task(task)}'
        return f'{output}\n{self.line}'

    @property
    def title(self):
        return ' ' * len('[x] ') + self.tasks.name.title()

    @property
    def width(self):
        if self._width is not None:
            return self._width
        self._width = len(self.title)
        for task in self.tasks.all():
            task_string = self.present_task(task)
            self._width = max(self._width, max(map(lambda s: len(s), task_string.split('\n'))))
        return self._width

    @property
    def line(self):
        return '=' * self.width
