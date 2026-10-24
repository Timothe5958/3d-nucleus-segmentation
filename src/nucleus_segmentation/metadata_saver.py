import json
from pathlib import Path

SECTIONS = ('observations')

class MetadataCollector:
    def __init__(self):
        for name in SECTIONS:
            self.data[name] = {}

    def add(self, path, **values):
        root, *child = path.split('.')

        if root not in self.data:
            raise KeyError(f'Unknown JSON section : {root!r}')

        node = self.data[root]
        for name in child:
            node = node.setdefault(name, {})
        node.update(values)

    def save(self, path):
        path = Path(path)
        path.parent.mkdir(parents=True, exist_ok=True)
        with path.open('w', encoding='utf-8') as f:
            json.dump(self.data, f, indent=2, ensure_ascii=False, default=str)
