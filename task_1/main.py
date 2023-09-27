from typing import Any

import yaml


class Person:
    def __init__(self, kind, age):
        self.kind = kind
        self.age = age
        pass


class Pet:
    def __init__(self, name, age, is_man, height, pet, grades):
        self.name = name
        self.age = age
        self.is_man = is_man
        self.height = height
        self.pet = pet
        self.grades = grades


class Schema:
    def __init__(self, name: str, schema: dict[str, Any]):
        self.name = name
        self.fields = schema


class Serializer:
    def __init__(self, schemas: dict[str, Any]):
        self.schemas = schemas
        self.available_schemas = self.init_schemas()

    @classmethod
    def load_from_file(cls, path: str):
        with open(path, 'r') as file:
            schema = yaml.safe_load(file)
        return cls(schema)

    def init_schemas(self):
        schema_version = self.schemas.get("version", 1)
        schemas = []
        for schema_name, schema_data in self.schemas.items():
            if schema_name in "version":
                continue

            if schema_version == 1:
                schemas.append(Schema(schema_name, schema_data))

        return schemas

    def serialize(self, obj: Any):
        pass


if __name__ == "__main__":
    person = {
        "name": "Ivan",
        "age": 10,
        "is_man": False,
        "height": 100.5,
        "pet": {
            "type": "dog",
            "age": 5.7,
        },
    }
    a = 'schema.yml'


    def obj_dfs(visited, graph, current):
        nodes = list(graph.keys())

        visited.add(nodes[current])
        print(nodes[current], ': ', graph[nodes[current]])

        if isinstance(graph[nodes[current]], dict):
            obj_dfs(visited, graph[nodes[current]], 0)

        if current + 1 < len(nodes):
            current += 1
            obj_dfs(visited, graph, current)


    visited = set()
    obj_dfs(visited, person, 0)
