import json
from typing import Dict

from .abstract import IO


class JsonIO(IO):
    def load_from(self, path: str) -> Dict:
        file = open(path)
        content = file.read()
        file.close()
        return json.loads(content)

    def save_to(self, content: Dict, path: str):
        with open(path, 'w') as file:
            json.dump(content, file, indent=4, sort_keys=True)

    @property
    def extension(self):
        return '.json'
