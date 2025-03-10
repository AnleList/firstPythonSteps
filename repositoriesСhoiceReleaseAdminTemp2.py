import subprocess

# Команда для открытия нового окна cmd, запроса ввода и сохранения его в файл
# command = "set /p choice=&& echo. %choice% > temp.txt"

# Создаём временный .bat-файл
bat_script = """
@echo off
set /p choice=Введите текст: 
echo %choice% > temp.txt
"""

# Записываем скрипт в файл
with open("script.bat", "w") as f:
    f.write(bat_script)

# Запускаем .bat-файл в новом окне cmd
subprocess.Popen(["start", "cmd", "/k", "script.bat"], shell=True)


# """
# set /p choice=Введите текст:&& echo %choice% > temp.txt
# """


# Ждём, пока пользователь введёт данные и закроет окно
input("Нажмите Enter после того, как введёте текст и закроете окно cmd...")

# Читаем введённое значение из временного файла и записываем в input.txt
with open('temp.txt', 'r') as temp_file:
    user_input = temp_file.read().strip()

print(f"Введённый текст: {user_input}")
