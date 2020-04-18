from tasks import Tasks, SimpleTasks

from .abstract import Parser


class SimpleJsonParser(Parser):
    def load_empty(self, name) -> SimpleTasks:
        return SimpleTasks(name)

    def load(self, content: dict) -> SimpleTasks:
        tasks_name = content['group']
        tasks = self.load_empty(tasks_name)
        for task_item in content['tasks']:
            task = tasks.add(task_item['name'])
            if task_item["done"]:
                task.finish()
        return tasks

    def dump(self, tasks: Tasks) -> dict:
        content = {
            "group": tasks.name,
            "tasks": [
                {
                    "name": task.name,
                    "done": task.done
                }
                for task in tasks.all()
            ]
        }
        return content
