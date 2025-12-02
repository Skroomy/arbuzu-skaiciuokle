import os
import json

def get_base_path():
    return os.path.abspath(__file__)[:-13]

class File:
    def __init__(self, name):
        self.path = get_base_path() + "data\\" + name + ".json"

    def write_json(self, data):
        with open(self.path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)

    def read_json(self):
        with open(self.path, "r", encoding="utf-8") as f:
            return json.load(f)