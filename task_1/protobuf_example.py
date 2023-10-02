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

# Сериализация объект  в бинарный формат
binary_Person = person.SerializeToString()

# Теперь мы можем использовать binary_Peson для передачи или хранения данных
with open("person.protobuf", "wb") as file:
  file.write(binary_Person)
