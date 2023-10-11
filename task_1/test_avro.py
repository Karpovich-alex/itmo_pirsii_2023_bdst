
import avro.schema
from avro.io import DatumWriter, DatumReader
from avro.datafile import DataFileWriter, DataFileReader
import tempfile
import numpy as np

from time import perf_counter_ns as time

schema = avro.schema.parse(open("schema.avsc", "rb").read())

temp_file_name = tempfile.NamedTemporaryFile().name

print("Run Avro")

times = np.array([])
for i in range(10_000):
    s = time()
    for _ in range(10):
        data = {"name": "Ivan", "age": 10, "is_man": True, "height": 100.5, "pet": {"kind": "dog", "age": 11.},
                "grades": [5, 4, 3], "add_data": {"0": {"abc": [1, 2, 3], "def": [123]}, "1": {"hij": [0]}}}
        writer = DataFileWriter(open(temp_file_name, "wb"), DatumWriter(), schema)
        writer.append(data)
    times = np.append(times, [(time()-s)/1e+6])
times = times/10
print("Serialize time:")
print(np.mean(times))
print(np.std(times))
print()

writer.close()

temp_file_name = tempfile.NamedTemporaryFile().name
writer = DataFileWriter(open(temp_file_name, "wb"), DatumWriter(), schema)
writer.append(data)
writer.flush()

times = np.array([])
for i in range(10_000):
    s = time()
    for _ in range(10):
        reader = DataFileReader(open(temp_file_name, "rb"), DatumReader())
        for user in reader:
            pass
    times = np.append(times, [(time()-s)/1e+6])
times = times/10
print("Deserialize time:")
print(np.mean(times))
print(np.std(times))



