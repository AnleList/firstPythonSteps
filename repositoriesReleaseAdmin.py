import requests
from bs4 import BeautifulSoup
from packaging import version
import subprocess
import re
from urllib.parse import unquote
import ctypes
import sys
import time
import threading
from datetime import datetime  # Импортируем модуль для работы с временем


# Функция для проверки прав администратора
def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False


# Если скрипт не запущен с правами администратора, перезапустить его
if not is_admin():
    print("Запуск с повышенными привилегиями...")
    ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)
    sys.exit()

# Базовый URL
base_url = 'https://files.hi-tech.org/desktop/iva_connect/release/'

# Модификаторы для запуска установщика
runKey = ['/SILENT', '/CURRENTUSER']  # Модификаторы можно изменить здесь

# Интервал проверки обновлений (в секундах)
updateTime = 3600  # 1 час (можно изменить на нужное значение)

# Флаг для остановки цикла
stop_flag = False


# Функция для получения списка версий
def get_versions(url):
    response = requests.get(url)
    if response.status_code != 200:
        print(f'Ошибка: {response.status_code}')
        return []

    soup = BeautifulSoup(response.text, 'html.parser')
    versions = []

    # Ищем все ссылки на странице
    for link in soup.find_all('a'):
        href = link.get('href')
        if href and href.endswith('/'):  # Папки версий заканчиваются на '/'
            version_str = href.rstrip('/')  # Убираем '/' в конце
            # Проверяем, что это версия (например, "15.0" или "21.4_rc")
            if version_str.replace('.', '').replace('_rc', '').isdigit():
                versions.append(version_str)

    return versions


# Функция для получения самого нового файла в папке
def get_latest_file_in_folder(folder_url):
    response = requests.get(folder_url)
    if response.status_code != 200:
        print(f'Ошибка: {response.status_code}')
        return None

    soup = BeautifulSoup(response.text, 'html.parser')
    files = []

    # Ищем все ссылки на файлы
    for link in soup.find_all('a'):
        href = link.get('href')
        if href and href.endswith('.exe'):  # Ищем только .exe файлы
            file_name = unquote(href)  # Декодируем URL
            # Извлекаем версию из названия файла с помощью регулярного выражения
            match = re.search(r'(\d+\.\d+\.\d+)', file_name)
            if match:
                version_str = match.group(1)  # Извлекаем версию (например, "21.5.5341")
                files.append((file_name, version.parse(version_str)))

    if files:
        # Сортируем по версии (от старшей к младшей)
        files.sort(key=lambda x: x[1], reverse=True)
        return files[0][0]  # Возвращаем имя файла с самой старшей версией
    return None


# Функция для сравнения версий с учетом _rc
def parse_version(v):
    # Удаляем _rc для сравнения, но сохраняем для выбора папки
    return version.parse(v.replace('_rc', ''))


# Основной цикл проверки обновлений
def check_for_updates():
    global stop_flag
    while not stop_flag:
        # Получаем текущее время
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f'[{current_time}] Проверка обновлений... (следующая проверка через {updateTime} секунд)')

        # Получаем список всех версий
        versions = get_versions(base_url)
        if not versions:
            print('Версии не найдены.')
            time.sleep(updateTime)
            continue

        # Выбираем самую старшую версию с учетом _rc
        latest_version = max(versions, key=lambda x: parse_version(x))
        print(f'Самая старшая версия: {latest_version}')

        # Переходим в папку с этой версией
        version_url = base_url + latest_version + '/'

        # Получаем самый новый файл в этой папке
        latest_file_name = get_latest_file_in_folder(version_url)
        if not latest_file_name:
            print('Файлы .exe не найдены в папке версии.')
            time.sleep(updateTime)
            continue

        # Скачиваем файл
        latest_file_url = version_url + latest_file_name
        print(f'Скачивание файла: {latest_file_name}')
        file_response = requests.get(latest_file_url)

        if file_response.status_code == 200:
            # Сохраняем файл на диск
            with open(latest_file_name, 'wb') as file:
                file.write(file_response.content)
            print(f'Файл успешно скачан: {latest_file_name}')

            # Запускаем скачанный файл с модификаторами из переменной runKey
            try:
                print(f'Запуск файла: {latest_file_name} с ключами {runKey}')
                subprocess.run([latest_file_name] + runKey, check=True)
            except subprocess.CalledProcessError as e:
                print(f'Ошибка при запуске файла: {e}')
            except FileNotFoundError:
                print(f'Файл не найден: {latest_file_name}')
        else:
            print(f'Ошибка при скачивании файла: {file_response.status_code}')

        # Ждем указанное количество секунд перед следующей проверкой
        time.sleep(updateTime)


# Запуск проверки обновлений в отдельном потоке
update_thread = threading.Thread(target=check_for_updates)
update_thread.start()

# Ожидание ввода пользователя для выхода
print("Программа проверки обновлений запущена. Введите любой символ (или текст) для выхода...")
input()  # Ожидаем ввод пользователя

# Устанавливаем флаг для остановки цикла
stop_flag = True
print("Завершение работы программы...")

# Ожидаем завершения потока
update_thread.join()
print("Программа завершена.")