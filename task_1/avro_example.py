import avro.schema
from avro.io import DatumWriter, DatumReader
from avro.datafile import DataFileWriter, DataFileReader
import tempfile
from time import time_ns as time


schema = avro.schema.parse(open("schema.avsc", "rb").read())
temp_file_name = tempfile.NamedTemporaryFile("wb", delete=False).name
s = time()
for i in range(100):
    writer = DataFileWriter(open(temp_file_name, "wb"), DatumWriter(), schema)
    data = {"name": "Ivan", "age": 10, "is_man": True, "height": 100.5, "pet": {"kind": "dog", "age": 11.}, "grades": [5, 4, 3], "add_data": {"0": {"abc": [1, 2, 3], "def": [123]}, "1": {"hij": [0]}}}

    writer.append(data)
print((time()-s)/1e+6)
writer.flush()
print((time()-s)/1e+6)
reader = DataFileReader(open(temp_file_name, "rb"), DatumReader())
for user in reader:
    print(user)
reader.close()
print((time()-s)/1e+6)