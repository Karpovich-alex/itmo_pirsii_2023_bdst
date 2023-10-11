import numpy as np

from time import perf_counter_ns as time
import protoc_files.task_1.schema_1_pb2 as person_pb2

from google.protobuf.json_format import MessageToJson

# Создаем объект Person
print("Run Protobuf")

times = np.array([])
for i in range(10_000):
    s = time()
    for _ in range(10):
        person = person_pb2.Person()
        person.name = "Ivan"
        person.age = 10
        person.is_man = True
        person.height = 100.5
        person.grades.extend([5, 4, 3])

        add_data_1 = person.add_data.add()
        add_data_1.key = 0
        add_data_1_1 = add_data_1.add_data_level_1.add()
        add_data_1_1.key = "abc"
        add_data_1_1.values.extend([1, 2, 3])

        add_data_1_2 = add_data_1.add_data_level_1.add()
        add_data_1_2.key = "def"
        add_data_1_2.values.extend([123])

        add_data_2 = person.add_data.add()
        add_data_2.key = 1
        add_data_2_1 = add_data_2.add_data_level_1.add()
        add_data_2_1.key = "hij"
        add_data_2_1.values.extend([0])
        ser_obj = person.SerializeToString()
    times = np.append(times, [(time() - s) * 1e-6])
times = times / 10
print("Serialize time:")
print(np.mean(times))
print(np.std(times))
print()

person = person_pb2.Person()

times = np.array([])
for i in range(10_000):
    s = time()
    for _ in range(10):
        person.ParseFromString(ser_obj)
        MessageToJson(person)
    times = np.append(times, [(time() - s) * 1e-6])
times = times / 10
print("Deserialize time:")
print(np.mean(times))
print(np.std(times))
