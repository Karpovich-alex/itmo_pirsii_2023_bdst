import numpy as np

from time import perf_counter_ns as time
from main import Serializer
from task_1.schema import Person, Pet

path_to_schema = 'schema.yml'
serializer = Serializer.load_from_file(path_to_schema, [Person, Pet])
pet = Pet("dog", 11.)
person = Person("Ivan", 10, True, 100.5, pet, [5, 4, 3], {0: {"abc": [1, 2, 3], "def": [123]},
                                                          1: {"hij": [0]}})

print("Run Our code")

times = np.array([])
for i in range(10_000):
    s = time()
    for _ in range(10):
        ser_obj = serializer.serialize(person)
    e = (time()-s)
    times = np.append(times, [e*1e-6])
times = times/10
print("Serialize time:")
print(np.mean(times))
print(np.std(times))
print()

times = np.array([])
for i in range(100_000):
    s = time()
    for _ in range(10):
        deser_obj = serializer.deserialize(ser_obj)
    times = np.append(times, [(time()-s)*1e-6])
times = times/10
print("Deserialize time:")
print(np.mean(times))
print(np.std(times))



