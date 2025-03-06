import requests

# URL страницы, которую вы хотите получить
url = 'https://files.hi-tech.org/desktop/iva_connect/beta/master/'

# Отправляем GET-запрос к странице
response = requests.get(url)

# Проверяем, что запрос был успешным (статус код 200)
if response.status_code == 200:
    # Получаем содержимое страницы
    content = response.text
    print(content)
else:
    print(f'Ошибка: {response.status_code}')