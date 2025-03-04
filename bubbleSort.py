import sys


def bubble_sort(arr):
    n = len(arr)
    for i in range(n):
        for j in range(0, n - i - 1):
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Использование: python script.py <число1> <число2> ... <числоN>")
        sys.exit(1)

    try:
        # Преобразуем аргументы командной строки в список целых чисел
        numbers = list(map(int, sys.argv[1:]))

        # Сортируем список методом пузырька
        bubble_sort(numbers)

        # Выводим отсортированный список
        print("Отсортированный список:", numbers)
    except ValueError:
        print("Ошибка: Все аргументы должны быть целыми числами.")