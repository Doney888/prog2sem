import os
import time
import stat

script_dir = os.path.dirname(os.path.abspath(__file__))
if os.getcwd() != script_dir:
    os.chdir(script_dir)

file_name = "example.txt"
with open(file_name, 'w') as file:
    file.write("This is an example file.\nHello, world of files!")

if not os.path.exists(file_name):
    print("FileNotFoundError: No such file or directory")
    exit(1)

file_stats = os.stat(file_name)
print(f"Информация о файле '{file_name}':")
print(f"Размер: {file_stats.st_size} байт")
print(f"Последнее изменение: {time.ctime(file_stats.st_mtime)}")
print(f"Последний доступ: {time.ctime(file_stats.st_atime)}")

print(f"Текущий пользователь: {os.getlogin()}")

print("\nИсходные права доступа:", oct(file_stats.st_mode)[-3:])

new_permissions = file_stats.st_mode | stat.S_IXUSR
os.chmod(file_name, new_permissions)

updated_stats = os.stat(file_name)
print("Новые права доступа:", oct(updated_stats.st_mode)[-3:])