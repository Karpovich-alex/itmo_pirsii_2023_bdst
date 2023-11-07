import avro.schema
from avro.datafile import DataFileReader, DataFileWriter
from avro.io import DatumReader, DatumWriter
from fastavro import writer, reader, parse_schema

# Загрузка схемы из файла
schema = avro.schema.Parse(open("person.avsc").read())

# Сериализация данных
writer = DataFileWriter(open("people.avro", "wb"), DatumWriter(), schema)
writer.append({"name": "Alice", "age": 30, "address": "123 Main St"})
writer.append({"name": "Bob", "age": 25, "address": "456 Elm St"})
writer.close()

# Десериализация данных
reader = DataFileReader(open("people.avro", "rb"), DatumReader())
for person in reader:
    print(person)
reader.close()
