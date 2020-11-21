import json
from pathlib import Path


def cfg_create(filename: Path):
    print(
        """Конфигурационный файл не найден. Желаете его создать? Y/N 
    """
    )
    decision = str(input())
    if decision in "Yy":
        Path(filename).touch()
        print(f"""Файл {filename} создан.""")
        json_parse(filename)
    elif decision in "Nn":
        print("""Завершаю работу...""")
    else:
        print("""Введен неверный символ. Повторите попытку""")


def json_find(filename: Path):
    if filename.exists():
        print("""Конфигурационный файл уже существует""")
    else:
        cfg_create(filename)


def json_parse(filename: Path):
    print("""Введите TOKEN, полученный у BotFather """)
    token = str(input())
    with open(filename, "w") as file:
        json.dump(token, file)
    print("""Токен был записан. Настройка завершена""")


if __name__ == "__main__":
    print(
        """
_________         _________ _        _        ______   _______  _______ 
\__   __/|\     /|\__   __/( (    /|| \    /\(  __  \ (  ____ \(  ____ )
   ) (   | )   ( |   ) (   |  \  ( ||  \  / /| (  \  )| (    \/| (    )|
   | |   | (___) |   | |   |   \ | ||  (_/ / | |   ) || (__    | (____)|
   | |   |  ___  |   | |   | (\ \) ||   _ (  | |   | ||  __)   |     __)
   | |   | (   ) |   | |   | | \   ||  ( \ \ | |   ) || (      | (\ (   
   | |   | )   ( |___) (___| )  \  ||  /  \ \| (__/  )| (____/\| ) \ \__
   )_(   |/     \|\_______/|/    )_)|_/    \/(______/ (_______/|/   \__/
"""
    )
    print(
        """Вас приветствует мастер настройки "Thinkder bot". Пытаюсь найти конфигурационный файл...
    """
    )
    json_find(Path("config.json"))
