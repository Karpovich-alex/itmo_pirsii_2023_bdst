import numpy as np

from time import perf_counter_ns as time
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

print("Run Protobuf")

times = np.array([])
for i in range(10_000):
    s = time()
    for _ in range(10):
        ser_obj = person.SerializeToString()
    times = np.append(times, [(time()-s)*1e-6])
times = times/10
print("Serialize time:")
print(np.mean(times))
print(np.std(times))
print()


times = np.array([])
for i in range(10_000):
    s = time()
    for _ in range(10):
        deser_obj = person.ParseFromString(ser_obj)
    times = np.append(times, [(time()-s)*1e-6])
times = times/10
print("Deserialize time:")
print(np.mean(times))
print(np.std(times))



