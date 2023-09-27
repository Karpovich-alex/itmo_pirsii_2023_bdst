import struct

nums = [1, 2, 3, 4, 5]

buf = bytearray()

for el in nums[::-1]:
    buf.extend(struct.pack("h", el))
print(buf)

# Записываем в файл числа
with open("test_file.b", "wb") as file:
    file.write(buf)

# Читаем числа из файла
with open("test_file.b", "rb") as file:
    read_buf = file.readline()
print(read_buf)

# Выводим байты подряд
for b in read_buf:
    print(b)

print()

# Выводим по 2 байта
type_size = 2
for b in read_buf[::type_size]:
    # тк наш тип содержит 2 байта, то можем сразу преобразовать в числа
    print(b)
