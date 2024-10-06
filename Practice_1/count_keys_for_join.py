"""
Задание 5

Описание работы скрипта:
1. Функция count_keys: считывает данные из файла и считает количество записей для каждого ключа, сохраняя это в словаре key_count. Мы используем defaultdict(int), чтобы упрощенно увеличивать счетчик для каждого ключа.
2. Функция find_problematic_keys: после того как мы посчитали количество записей для каждого ключа в обоих файлах, проверяем каждый ключ на наличие проблем. Если в любой из таблиц количество записей по ключу больше 60000, ключ добавляется в множество проблемных ключей.
3. Основная функция main: организует работу:
    * Сначала вызываем count_keys для обоих файлов.
    * Затем находим ключи, которые могут вызвать проблемы.
4. Чтение файла: так как мы используем чтение файла построчно (а не полностью загружаем его в память), это позволяет работать с файлами, которые значительно превышают объем оперативной памяти.
5. Запись проблемных ключей: в конце мы сохраняем проблемные ключи в текстовый файл, чтобы их можно было просмотреть.
"""

import csv
from collections import defaultdict
import utils

# Константы
THRESHOLD = 60000


def count_keys(file_path, key_column=0):
    """
    Первый проход: Подсчитывает количество записей для каждого ключа в CSV-файле.
    Возвращает словарь с количеством записей по каждому ключу.
    """
    key_counts = defaultdict(int)

    # Чтение файла по частям (чтобы экономить память)
    with open(file_path, 'r') as f:
        reader = csv.reader(f)
        for row in reader:
            key = row[key_column]
            key_counts[key] += 1

    return key_counts


def find_problematic_keys(count1, count2):
    """Функция для нахождения ключей, которые вызывают проблему (больше THRESHOLD записей)."""
    problematic_keys = set()

    # Проверяем ключи из первой таблицы
    for key, count in count1.items():
        if count > THRESHOLD or count2.get(key, 0) > THRESHOLD:
            problematic_keys.add(key)

    # Проверяем ключи из второй таблицы, которых нет в первой
    for key, count in count2.items():
        if key not in count1 and count > THRESHOLD:
            problematic_keys.add(key)

    return problematic_keys


def main(file1, file2):
    # Шаг 1: Подсчет ключей в каждом файле
    print("Подсчет ключей в первом файле...")
    key_counts_file1 = count_keys(file1)

    print("Подсчет ключей во втором файле...")
    key_counts_file2 = count_keys(file2)

    # Нахождение ключей, которые могут вызвать проблемы
    print("Ищем проблемные ключи...")
    problematic_keys = find_problematic_keys(key_counts_file1, key_counts_file2)

    # Выводим проблемные ключи
    print(f"Найдено проблемных ключей: {len(problematic_keys)}")

    # Сохранение проблемных ключей в файл
    with open('problematic_keys.txt', 'w') as f:
        for key in problematic_keys:
            f.write(f"{key}\n")


def generate_test_data():
    """
    Генерирует тестовые CSV файлы для выполнения тестов.
    """
    print("Генерация тестовых данных...")

    # Генерация файла с группированными ключами (например, с повторяющимися ключами)
    pattern = [(10, 100_000)]  # Пример шаблона
    utils.gen_grouped_seq("file1.csv", pattern, n_extra_cols=0, to_shuffle=False)
    utils.gen_grouped_seq("file2.csv", pattern, n_extra_cols=0, to_shuffle=False)

    print("Тестовые данные сгенерированы: 'file1.csv', 'file2.csv'.")


if __name__ == "__main__":
    # Шаг 1: Генерация данных
    generate_test_data()

    # Шаг 2: Выполнение основного процесса - подсчет и JOIN
    file1 = 'file1.csv'
    file2 = 'file2.csv'

    main(file1, file2)
