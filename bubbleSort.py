def bubble_sort(arr):
    n = len(arr)
    for i in range(n):
        for j in range(n - i - 1):
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]


if __name__ == "__main__":
    try:
        # Запрашиваем ввод чисел у пользователя
        input_str = input("Введите числа через пробел: ")

        # Преобразуем введенные данные в список целых чисел
        numbers = list(map(int, input_str.split()))

        # Сортируем список методом пузырька
        bubble_sort(numbers)

        # Выводим отсортированный список
        print("Отсортированный список:", numbers)
    except ValueError:
        print("Ошибка: Введите только числа, разделенные пробелами.")