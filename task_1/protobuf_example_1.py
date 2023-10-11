import protoc_files.task_1.schema_1_pb2 as person_pb2

# Создаем объект Person
person = person_pb2.Person()
person.name = "Ivan"
person.age = 10
person.is_man = True
person.height = 100.5
person.grades.extend([5, 4, 3])

add_data_1 = person.add_data.add()
add_data_1.key = 0
add_data_1_1 = add_data_1.add_data_level_1.add()
add_data_1_1.key ="abc"
add_data_1_1.values.extend([1, 2, 3])

add_data_1_2 = add_data_1.add_data_level_1.add()
add_data_1_2.key ="def"
add_data_1_2.values.extend([123])

add_data_2 = person.add_data.add()
add_data_2.key=1
add_data_2_1 = add_data_2.add_data_level_1.add()
add_data_2_1.key ="hij"
add_data_2_1.values.extend([0])

# Создаем объект Pet + установка значений
pet = person.pet
pet.type = "dog"
pet.age = 11.0

# Сериализация объект  в бинарный формат
binary_Person = person.SerializeToString()

# Теперь мы можем использовать binary_Peson для передачи или хранения данных
with open("person.protobuf", "wb") as file:
  file.write(binary_Person)

with open("person.protobuf", "rb") as file:
  br = file.read()
print(person.ParseFromString(br))