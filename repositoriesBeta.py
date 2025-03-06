import requests
from bs4 import BeautifulSoup
from packaging import version
import subprocess

# URL страницы
url = 'https://files.hi-tech.org/desktop/iva_connect/beta/master/'

# Получаем содержимое страницы
response = requests.get(url)
if response.status_code != 200:
    print(f'Ошибка: {response.status_code}')
    exit()

# Парсим HTML
soup = BeautifulSoup(response.text, 'html.parser')

# Список для хранения информации о файлах
exe_files = []

# Ищем все ссылки на странице
for link in soup.find_all('a'):
    href = link.get('href')
    if href and href.endswith('.exe'):
        # Извлекаем имя файла и версию
        file_name = href
        # Удаляем суффиксы, такие как _x86, перед парсингом версии
        version_str = file_name.split('beta-')[1].split('.exe')[0]
        version_str = version_str.split('_')[0]  # Удаляем всё после символа '_'
        exe_files.append((file_name, version.parse(version_str)))

# Если найдены .exe файлы
if exe_files:
    # Сортируем по версии (от старшей к младшей)
    exe_files.sort(key=lambda x: x[1], reverse=True)

    # Выбираем файл с самой старшей версией
    latest_file = exe_files[0]
    latest_file_name = latest_file[0]
    latest_file_url = url + latest_file_name

    print(f'Найден файл с самой старшей версией: {latest_file_name}')

    # Скачиваем файл
    print(f'Скачивание файла: {latest_file_name}')
    file_response = requests.get(latest_file_url)

    if file_response.status_code == 200:
        # Сохраняем файл на диск
        with open(latest_file_name, 'wb') as file:
            file.write(file_response.content)
        print(f'Файл успешно скачан: {latest_file_name}')

        # Запускаем скачанный файл
        try:
            print(f'Запуск файла: {latest_file_name}')
            subprocess.run([latest_file_name], check=True)
        except subprocess.CalledProcessError as e:
            print(f'Ошибка при запуске файла: {e}')
        except FileNotFoundError:
            print(f'Файл не найден: {latest_file_name}')
    else:
        print(f'Ошибка при скачивании файла: {file_response.status_code}')
else:
    print('Файлы .exe не найдены.')