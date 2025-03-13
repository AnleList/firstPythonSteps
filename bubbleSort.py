def bubble_sort(arr) -> list[int]:
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
        sortedList = bubble_sort(numbers)

        # Выводим отсортированный список
        print("Отсортированный список:", sortedList)
    except ValueError:
        print("Ошибка: Введите только числа, разделенные пробелами.")