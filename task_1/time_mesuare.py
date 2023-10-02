import timeit
import numpy as np
from tabulate import tabulate
from time import perf_counter_ns

setup_our_code = \
"""from main import Serializer
from task_1.schema import Person, Pet
path_to_schema = 'schema.yml'
serializer = Serializer.load_from_file(path_to_schema, [Person, Pet])
pet = Pet("dog", 11.)
person = Person("Ivan", 10, True, 100.5, pet, [5, 4, 3])"""

setup_our_code_deserialize = \
"""
ser_obj = serializer.serialize(person)"""

serialize_our_code = \
"""def test_our_code():
    serializer.serialize(person)"""

deserialize_our_code = \
"""def test_our_code():
    serializer.deserialize(ser_obj)"""

setup_protobuf = \
"""import protoc_files.task_1.schema_pb2 as person_pb2

# Создаем объект Person
person = person_pb2.Person()
person.name = "Ivan"
person.age = 10
person.is_man = True
person.height = 100.5
grade = person.grades.add()
grade.number = 5
grade = person.grades.add()
grade.number = 4
grade = person.grades.add()
grade.number = 3
# Создаем объект Pet + установка значений
pet = person.pet
pet.type = "dog"
pet.age = 11.0"""

setup_protobuf_deserialize = \
"""
ser_obj = person.SerializeToString()"""

serialize_protobuf = \
"""def test_protobuf():
    person.SerializeToString()"""
deserialize_protobuf = \
"""person.ParseFromString(ser_obj)"""


our_ser_size = 0
proto_ser_size = 0


def get_our_ser_size():
    from main import Serializer
    from task_1.schema import Person, Pet
    path_to_schema = 'schema.yml'
    serializer = Serializer.load_from_file(path_to_schema, [Person, Pet])
    pet = Pet("dog", 11.)
    person = Person("Ivan", 10, True, 100.5, pet, [5, 4, 3])
    ser_obj = serializer.serialize(person)
    return len(ser_obj)


def get_protobuf_ser_size():
    import protoc_files.task_1.schema_pb2 as person_pb2

    # Создаем объект Person
    person = person_pb2.Person()
    person.name = "Ivan"
    person.age = 10
    person.is_man = True
    person.height = 100.5
    grade = person.grades.add()
    grade.number = 5
    grade = person.grades.add()
    grade.number = 4
    grade = person.grades.add()
    grade.number = 3
    # Создаем объект Pet + установка значений
    pet = person.pet
    pet.type = "dog"
    pet.age = 11.0
    ser_obj = person.SerializeToString()
    return len(ser_obj)


def add_main_header(table):
    rows = table.split("\n")
    header_row = rows[0]
    cells = header_row.split("|")
    new_header = "|".join(cells[:2])
    new_header += "|{0}".format(format(cells[4].strip(), f' ^{len(cells[2]) + len(cells[3]) + 1}'))
    new_header += "|{0}".format(format(cells[5].strip(), f' ^{len(cells[4]) + len(cells[5]) + 1}')) + "|"
    new_header += "|".join(cells[6:])
    rows[0] = new_header
    rows.insert(3, rows[1])
    return "\n".join(rows)


our_ser_size = get_our_ser_size()
proto_ser_size = get_protobuf_ser_size()

number = 100_000
our_time_ser = np.array(timeit.repeat(setup=setup_our_code, stmt=serialize_our_code, number=number, timer=perf_counter_ns))*1e-6
protobuf_time_ser = np.array(timeit.repeat(setup=setup_protobuf, stmt=serialize_protobuf, number=number, timer=perf_counter_ns))*1e-6

our_time_deser = np.array(
    timeit.repeat(setup=setup_our_code + setup_our_code_deserialize, stmt=deserialize_our_code, number=number, timer=perf_counter_ns))*1e-6
protobuf_time_deser = np.array(
    timeit.repeat(setup=setup_protobuf + setup_protobuf_deserialize, stmt=deserialize_protobuf, number=number, timer=perf_counter_ns))*1e-6


floatfrmt = "{:.5f}"
table = tabulate([["Name", "mean", "std", "mean", "std", "size (bytes)"],
                  ["our_code", floatfrmt.format(np.mean(our_time_ser)), floatfrmt.format(np.std(our_time_ser)),
                   floatfrmt.format(np.mean(our_time_deser)), floatfrmt.format(np.std(our_time_deser)), our_ser_size],
                  ["protobuf", floatfrmt.format(np.mean(protobuf_time_ser)), floatfrmt.format(np.std(protobuf_time_ser)),
                   floatfrmt.format(np.mean(protobuf_time_deser)), floatfrmt.format(np.std(protobuf_time_deser)),
                   proto_ser_size]],
                 headers=["", "serialization (ms)", "deserialization (ms)", ""],
                 tablefmt="github",
                 disable_numparse=True)
table = add_main_header(table)
print(table)
