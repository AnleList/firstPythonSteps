import requests
from bs4 import BeautifulSoup
from packaging import version
import subprocess
import re
from urllib.parse import unquote
import ctypes
import sys

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
runKey = ['/SILENT', '/AllUsers']  # Модификаторы можно изменить здесь

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

# Получаем список всех версий
versions = get_versions(base_url)
if not versions:
    print('Версии не найдены.')
    exit()

# Функция для сравнения версий с учетом _rc
def parse_version(v):
    # Удаляем _rc для сравнения, но сохраняем для выбора папки
    return version.parse(v.replace('_rc', ''))

# Выбираем самую старшую версию с учетом _rc
latest_version = max(versions, key=lambda x: parse_version(x))
print(f'Самая старшая версия: {latest_version}')

# Переходим в папку с этой версией
version_url = base_url + latest_version + '/'

# Получаем самый новый файл в этой папке
latest_file_name = get_latest_file_in_folder(version_url)
if not latest_file_name:
    print('Файлы .exе не найдены в папке версии.')
    exit()

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