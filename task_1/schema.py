__all__ = ["Pet", "Person"]


class Pet:
    _schema_name = "pet"
    _schema_version = 1

    def __init__(self, kind, age):
        self.kind = kind
        self.age = age
        pass


class Person:
    _schema_name = "person"
    _schema_version = 1

    def __init__(self, name: str, age: int, is_man: bool, height: float, pet: Pet, grades: int):
        self.name = name
        self.age = age
        self.is_man = is_man
        self.height = height
        self.pet = pet
        self.grades = grades
