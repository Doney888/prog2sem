import os

def create_file(path, content):
    """
    Функция для создания файла
    :param path: путь к файлу
    :param content: содержание файла
    """
    with open(path, 'w') as f:
        f.write(content)


script_dir = os.path.dirname(os.path.abspath(__file__))
if os.getcwd() != script_dir:
    os.chdir(script_dir)
print(f"Текущая директория: {os.getcwd()}")

original_file = "example.txt"
copied_file = "example_copy.txt"

if os.path.exists(original_file):
    with open(original_file, 'r') as src, open(copied_file, 'w') as dst:
        dst.write(src.read())

renamed_file = "renamed_example.txt"
os.rename(copied_file, renamed_file)

nested_dir = os.path.join("dir1", "dir2", "dir3")
os.makedirs(nested_dir, exist_ok=True)

moved_file = os.path.join(nested_dir, "moved_file.txt")
os.rename(renamed_file, moved_file)

new_file = "temp_file.txt"
create_file(new_file, "Временный файл")

new_location = os.path.join(nested_dir, "permanent_file.txt")
os.rename(new_file, new_location)

for i in range(1, 4):
    create_file(f"file_{i}.txt", f"Содержимое файла {i}")

print("\nСодержимое корневой директории:")
for item in os.listdir():
    full_path = os.path.join(os.getcwd(), item)
    print(f"{item} - {'папка' if os.path.isdir(full_path) else 'файл'}")

os.chdir(nested_dir)
print(f"\nПерешли в директорию: {os.getcwd()}")
print("Содержимое вложенной директории:")
for item in os.listdir():
    print(f"  {item}")

os.chdir(script_dir)
print(f"\nВернулись в: {os.getcwd()}")

empty_dir = "temp_dir"
os.makedirs(empty_dir, exist_ok=True)
os.rmdir(empty_dir)

deep_nested = os.path.join("project", "src", "utils")
os.makedirs(deep_nested, exist_ok=True)

create_file(os.path.join("project", "README.md"), "# Проект")
create_file(os.path.join("project", "src", "main.py"), "print('Hello')")
create_file(os.path.join("project", "src", "utils", "helpers.py"), "def help(): pass")

print("\nРекурсивный обход директории:")
for root, dirs, files in os.walk(script_dir):
    # Пропускаем служебные директории
    if '__pycache__' in root:
        continue

    print(f"\nДиректория: {os.path.relpath(root, script_dir)}")

    if dirs:
        print("  Поддиректории: " + ", ".join(dirs))

    if files:
        print("  Файлы: " + ", ".join(files))
    else:
        print("  Файлов нет")