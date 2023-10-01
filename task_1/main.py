import struct
from typing import Any

import yaml

from task_1.schema import Person, Pet


class Schema:
    def __init__(self, name: str, schema: dict[str, Any]):
        self.name = name
        self.fields = schema


class Serializer:
    """
    Класс содержит информацию о всех классах и их схемах
    имеет методы
    serialize и deserialize

    """

    def __init__(self, schemas: dict[str, Any], classes: list | None = None):

        # {(schema_name, schema_version): schema, ...}
        self.schemas = self.init_schemas(schemas)

        # {(schema_name, schema_version): class_obj, ...}
        self._classes = [] if classes is None else self.init_classes(classes)

        self.class_matcher = {
            "int": "q",
            "bool": "?",
            "float": "d",
        }
        self.type_matcher = {
            "bool": bool,
            "str": str,
            "int": int,
            "float": float,
            "list": list,
            "dict": dict,
        }
        self.str_encoding = "UTF-8"

    @property
    def classes(self):
        return self._classes

    @classes.setter
    def classes(self, values):
        self._classes = self.init_classes(values)

    @classes.getter
    def classes(self):
        return self._classes

    @classmethod
    def load_from_file(cls, path: str, classes: list[object]):
        with open(path, 'r') as file:
            schema = yaml.safe_load(file)
        return cls(schema, classes)

    def init_schemas(self, schemas: dict[str, Any]):
        parsed_schemas = {}
        for schema_name, schema_data in schemas.items():
            schema_version = schema_data.pop("version", 1)
            parsed_schemas[(schema_name, schema_version)] = schema_data

        return parsed_schemas

    def init_classes(self, classes: list[Person | Pet]):
        parsed_classes = {}
        for class_obj in classes:
            schema_name = getattr(class_obj, "_schema_name")
            schema_version = getattr(class_obj, "_schema_version")
            parsed_classes[(schema_name, schema_version)] = class_obj

        return parsed_classes

    def deserialize(self, obj: Any, path: str):
        """
        Преобразует файл в объект
        :param obj: Класс, который находится в файле path
        :param path: Путь до файла
        :return:
        """
        pass

    def get_type_by_name(self, type_name: str):
        type_instance = self.type_matcher.get(type_name, None)
        if type_instance:
            return type_instance

        # Фильтруем все переданные классы, получаем их ключи и значения (объекты класса)
        type_instance = list(filter(lambda x: x[0][0] == type_name,
                                    self.classes.items()))
        if not type_instance:
            raise AttributeError("Cant find type_instance")

        # Выбираем первый элемент списка и отдаем класс
        return type_instance[0][1]

    def serialize(self, obj: Person) -> bytes:  # , path: str
        """
        Преобразует объект в сериализованный фалй
        :param obj: Экземпляр класса, который требуется сериализовать
        :param path: Путь до папки, в которую требуется сохранить файл
        :return:
        """
        schema_version = obj._schema_version
        schema_name = obj._schema_name
        obj_schema = self.schemas.get((obj._schema_name, schema_version))
        serialized_data = bytearray()
        main_buffer = bytearray()
        # Добавляем название и версию схемы
        main_buffer.extend(self._serialize(schema_name))
        main_buffer.extend(self._serialize(schema_version))

        for field_name, field_metadata in sorted(list(obj_schema.items()), key=lambda x: x[1]["id"]):
            field_value = getattr(obj, field_name)
            # TODO: int может быть указано в схеме как float
            assert isinstance(field_value, self.get_type_by_name(field_metadata["type"])), \
                "field type in class doesnt match type in schema"
            serialized_field = self._serialize(field_value)
            serialized_data.extend(serialized_field)
            main_buffer.extend(self._serialize(len(serialized_field)))
        main_buffer.extend(serialized_data)
        return main_buffer

    def _serialize(self, obj: Any, pack_params=None) -> bytes:
        """
        Возвращает сериализованный объект (байты)
        :param obj:
        :return:
        """
        if pack_params:
            return struct.pack(pack_params, obj)

        if isinstance(obj, int):
            return struct.pack(self.class_matcher["int"], obj)
        elif isinstance(obj, float):
            return struct.pack(self.class_matcher["float"], obj)
        elif isinstance(obj, str):
            return obj.encode(self.str_encoding)
        elif isinstance(obj, bool):
            return struct.pack(self.class_matcher["bool"], obj)
        else:
            return self.serialize(obj)


if __name__ == "__main__":
    # print(Person._schema_name)
    # person = {
    #     "name": "Ivan",
    #     "age": 10,
    #     "is_man": False,
    #     "height": 100.5,
    #     "pet": {
    #         "type": "dog",
    #         "age": 5.7,
    #     },
    # }
    path_to_schema = 'schema.yml'

    serializer = Serializer.load_from_file(path_to_schema, [Person, Pet])
    pet = Pet("dog", 11.)
    person = Person("Ivan", 10, True, 100.5, pet, 7)
    ser_obj = serializer.serialize(person)
    with open("person.d", "wb") as file:
        file.write(ser_obj)


    # print(a.serialize(123))
    # print(a.serialize("123"))
    # print(a.serialize(True))

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
