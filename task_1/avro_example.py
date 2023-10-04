
import avro.schema
from avro.datafile import DataFileReader, DataFileWriter
from avro.io import DatumReader, DatumWriter

schema = avro.schema.parse(open("schema.avsc", "rb").read())


writer = DataFileWriter(open("schema.avro", "wb"), DatumWriter(), schema)
writer.append({"name": "Ivan", "age": 10, "is_man": True, "height": 100.5, "pet": {"kind": "dog", "age": 11.}, "grades": [5, 4, 3], "add_data": {"0": {"abc": [1, 2, 3], "def": [123]}, "1": {"hij": [0]}}})
writer.close()

reader = DataFileReader(open("users.avro", "rb"), DatumReader())
for user in reader:
    print(user)
reader.close()



