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
        self._classes = {} if classes is None else self.init_classes(classes)

        self.class_matcher = {
            "int": "Q",
            "bool": "?",
            "float": "d",
            "str": "{0}p",
        }
        self.class_length = {
            "q": 8,
            "Q": 8,
            "?": 1,
            "d": 8,
            "L": 4,
            "B": 1,
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
        self._object_size_type = "L"

    @property
    def object_size_type(self):
        return self._object_size_type

    @object_size_type.setter
    def object_size_type(self, v):
        assert v in self.class_length, f"field type {v} doesnt have a length in class_length dict"
        self.object_size_type = v

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

    def init_classes(self, classes: list[Person | Pet]) -> dict[tuple[str, int], Any]:
        parsed_classes = {}
        for class_obj in classes:
            schema_name = getattr(class_obj, "_schema_name")
            schema_version = getattr(class_obj, "_schema_version")
            parsed_classes[(schema_name, schema_version)] = class_obj

        return parsed_classes

    def deserialize(self, bytes_data: bytes) -> Any:
        """
        Преобразует файл в объект
        :param obj: Класс, который находится в файле path
        :param path: Путь до файла
        :return:
        """
        schema_name, schema_version, end_position = self.get_schema_metadata(bytes_data)
        obj_schema = self.schemas.get((schema_name, schema_version))
        if not obj_schema:
            raise AttributeError("Cant find schema for (%s, %s)", schema_name, schema_version)
        obj = self.classes.get((schema_name, schema_version), None)
        if not obj:
            raise AttributeError("Cant find class for (%s, %s)", schema_name, schema_version)

        object_params = {}
        for field_name, field_metadata in sorted(list(obj_schema.items()), key=lambda x: x[1]["id"]):
            field_data, end_position = self._deserialize(bytes_data, field_metadata["type"],
                                                         start_position=end_position, pack_params=field_metadata)
            object_params[field_name] = field_data
            # TODO: Добавить проверку на версию схемы для классов

        return obj(**object_params)

    def get_schema_metadata(self, bytes_data) -> tuple[str, int, int]:
        schema_name, end_position = self._deserialize(bytes_data, "str", 0)
        schema_version, end_position = self._deserialize(bytes_data, "int", end_position)
        return schema_name, schema_version, end_position

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

    def serialize(self, obj: Person, add_obj_size=False) -> bytes:  # , path: str
        """
        Преобразует объект в сериализованный файл
        :param obj: Экземпляр класса, который требуется сериализовать
        :param path: Путь до папки, в которую требуется сохранить файл
        :return:
        """
        schema_version = obj._schema_version
        schema_name = obj._schema_name
        obj_schema = self.schemas.get((schema_name, schema_version))

        serialized_data = bytearray()
        main_buffer = bytearray()
        # Резервируем место под размер объекта
        if add_obj_size:
            # obj_size, schema_name, schema_version
            main_buffer.extend(self._serialize(0, pack_params=self.object_size_type))

        # Добавляем название и версию схемы
        main_buffer.extend(self._serialize(schema_name))
        assert isinstance(schema_version, int), "schema_version type should be int"
        main_buffer.extend(self._serialize(schema_version))

        for field_name, field_metadata in sorted(list(obj_schema.items()), key=lambda x: x[1]["id"]):
            field_value = getattr(obj, field_name)
            # TODO: int может быть указано в схеме как float
            # TODO: проверка типа элементов списка и словаря
            assert isinstance(field_value, self.get_type_by_name(field_metadata["type"])) or \
                   (type(field_value) == "float" and field_metadata["type"] == "float"), \
                "field type (%s) in class does not match type in schema" % type(field_value)
            serialized_field = self._serialize(field_value)
            # print('{:<12}  {:<12}'.format(field_name, serialized_field.hex()))
            serialized_data.extend(serialized_field)
        main_buffer.extend(serialized_data)
        if add_obj_size:
            obj_size_length = self.class_length[self.object_size_type]
            main_buffer[:obj_size_length] = self._serialize(len(main_buffer), pack_params=self.object_size_type)
        return main_buffer

    # def check_field_type(self, field_value, field_metadata):
    #     schema_type = self.get_type_by_name(field_metadata["type"])
    #     if field_metadata["type"] == "list":
    #         el_type = field_metadata["element_type"]
    #         if el_type in ("list", "dict"):
    #             self.check_field_type()
    #     elif field_metadata["type"] == "dict":
    #         el_type = field_metadata["element_type"]
    #         key_type = field_metadata["key_type"]
    #         for key, value in field_value.items():
    #             self.check_field_type(field_value, field_metadata["type"])
    #     else:  # проверяем int, float, bool, str, <class>
    #         assert isinstance(field_value, schema_type) or \
    #                (type(field_value) == "float" and field_metadata["type"] == "float")

    def _serialize(self, obj: Any, pack_params=None) -> bytes:
        """
        Возвращает сериализованный объект (байты)
        :param obj:
        :return:
        """
        if pack_params:
            return struct.pack(pack_params, obj)

        if isinstance(obj, bool):
            return struct.pack(self.class_matcher["bool"], obj)
        elif isinstance(obj, int):
            return struct.pack(self.class_matcher["int"], obj)
        elif isinstance(obj, float):
            return struct.pack(self.class_matcher["float"], obj)
        elif isinstance(obj, str):
            encoded_string = obj.encode(self.str_encoding)
            return struct.pack(self.class_matcher["str"].format(len(obj) + 1), encoded_string)
        elif isinstance(obj, list):
            num_elements = len(obj)

            buffer = bytearray()
            buffer.extend(self._serialize(num_elements, "B"))
            for el in obj:
                buffer.extend(self._serialize(el))
            return buffer
        elif isinstance(obj, dict):
            num_elements = len(obj.keys())

            buffer = bytearray()
            buffer.extend(self._serialize(num_elements, "B"))
            for key, el in obj.items():
                buffer.extend(self._serialize(key))
                buffer.extend(self._serialize(el))
            return buffer
        else:
            return self.serialize(obj, add_obj_size=True)

    def _deserialize(self, bytes_data: bytes, obj_type: str, start_position: int = 0, pack_params=None) -> Any:
        """
        Возвращает десериализованный объект и позицию, на которой объект закончился
        :param bytes_data:
        :param obj_type:
        :param start_position:
        :param pack_params:
        :return: (obj, end_position)
        """
        if not isinstance(obj_type, dict) and obj_type in self.class_length.keys():
            obj_len = self.class_length[obj_type]
            end_position = start_position + obj_len
            return struct.unpack(obj_type, bytes_data[start_position:end_position]), end_position

        if obj_type in ("int", "float", "bool"):
            obj_pack_param = self.class_matcher[obj_type]
            obj_len = self.class_length[obj_pack_param]
            end_position = start_position + obj_len
            return struct.unpack(obj_pack_param, bytes_data[start_position: end_position])[0], \
                end_position
        elif obj_type == "str":
            obj_len = struct.unpack("B", bytes_data[start_position:start_position + 1])[0] + 1
            end_position = start_position + obj_len
            unpacked_obj = struct.unpack(self.class_matcher["str"].format(obj_len),
                                         bytes_data[start_position: end_position])[0]
            return unpacked_obj.decode(self.str_encoding), end_position
        elif obj_type == "list":
            el_type = pack_params.get("element_type", None)
            el_element_type = None
            assert el_type, "element_type should be passed"
            if isinstance(el_type, dict):
                el_element_type = el_type
                el_type = el_type["type"]

            el_num = struct.unpack("B", bytes_data[start_position:start_position + 1])[0]

            end_position = start_position + 1
            unpacked_obj = []
            for _ in range(el_num):
                unpacked_obj_el, end_position = self._deserialize(bytes_data, el_type, end_position, el_element_type)
                unpacked_obj.append(unpacked_obj_el)
            return unpacked_obj, end_position
        elif obj_type == "dict":
            el_type = pack_params.get("element_type", None)
            el_element_type = None
            assert el_type, "element_type should be passed"
            if isinstance(el_type, dict):
                el_element_type = el_type
                el_type = el_type["type"]

            key_type = pack_params.get("key_type", None)
            assert el_type, "key_type should be passed"

            el_num = struct.unpack("B", bytes_data[start_position:start_position + 1])[0]

            end_position = start_position + 1
            unpacked_obj = {}
            for _ in range(el_num):
                unpacked_obj_key, end_position = self._deserialize(bytes_data, key_type, end_position, )
                unpacked_obj_el, end_position = self._deserialize(bytes_data, el_type, end_position, el_element_type)
                unpacked_obj[unpacked_obj_key] = unpacked_obj_el
            return unpacked_obj, end_position
        else:
            obj_len, end_position = self._deserialize(bytes_data, self.object_size_type, start_position, )
            obj_len = obj_len[0]
            unpacked_obj = self.deserialize(bytes_data[end_position: start_position + obj_len])
            return unpacked_obj, start_position + obj_len


if __name__ == "__main__":
    path_to_schema = 'schema.yml'

    serializer = Serializer.load_from_file(path_to_schema, [Person, Pet])
    pet = Pet("dog", 11.)
    person = Person("Ivan", 10, True, 100.5, pet, [5, 4, 3], {0: {"abc": [1, 2, 3], "def": [123]},
                                                              1: {"hij": [0]}})
    ser_obj = serializer.serialize(person)

    with open("person.d", "wb") as file:
        file.write(ser_obj)

    with open("person.d", "rb") as file:
        ser_obj = file.read()

    new_obj = serializer.deserialize(ser_obj)
    print(new_obj)
