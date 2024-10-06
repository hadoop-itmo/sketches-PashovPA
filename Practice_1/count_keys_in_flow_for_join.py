"""
Задание 6

Описание работы скрипта:
1. Bloom Filter используется для проверки наличия ключей из второго файла в первом. Это позволяет эффективно по памяти отсекать непересекающиеся ключи.
2. Count-Min Sketch применяется для грубой оценки частоты появления каждого ключа. С его помощью можно подсчитать примерное количество строк для каждого ключа.
3. Если в файле менее 1 миллиона уникальных ключей, результат пересечения считается точно с использованием хеш-таблиц. В остальных случаях результат оценивается.
4. Скрипт поддерживает работу с большими файлами, но при этом использует ограниченную память для обработки больших наборов данных.
"""

import mmh3
import numpy as np
import utils
import shutil


class BloomFilter:
    def __init__(self, size, num_hashes):
        self.size = size
        self.num_hashes = num_hashes
        self.bit_array = np.zeros(size, dtype=bool)

    def _hashes(self, key):
        return [mmh3.hash(key, i) % self.size for i in range(self.num_hashes)]

    def add(self, key):
        for h in self._hashes(key):
            self.bit_array[h] = True

    def contains(self, key):
        return all(self.bit_array[h] for h in self._hashes(key))


class CountMinSketch:
    def __init__(self, width, depth):
        self.width = width
        self.depth = depth
        self.table = np.zeros((depth, width), dtype=int)
        self.hashes = [lambda x, i=i: mmh3.hash(x, i) % width for i in range(depth)]

    def add(self, key):
        for i, h in enumerate(self.hashes):
            self.table[i][h(key)] += 1

    def estimate(self, key):
        return min(self.table[i][h(key)] for i, h in enumerate(self.hashes))


def read_file_with_bloom_filter(file_name, bloom_filter, sketch, max_keys):
    key_set = set()
    total_keys = 0

    with open(file_name, 'r') as f:
        for line in f:
            key = line.split(',')[0]  # Предполагается, что ключ — это первое поле
            if key not in key_set and total_keys < max_keys:
                key_set.add(key)
            bloom_filter.add(key)
            sketch.add(key)
            total_keys += 1

    return key_set


def estimate_join_size(file_name, bloom_filter, sketch):
    join_count = 0

    with open(file_name, 'r') as f:
        for line in f:
            key = line.split(',')[0]
            if bloom_filter.contains(key):
                join_count += sketch.estimate(key)

    return join_count


def main():
    # Генерация тестовых данных
    print("Generating test data...")

    # Файл с уникальными ключами
    pattern = [(10, 100_000)]
    file1 = "test_file1.csv"
    file2 = "test_file2.csv"
    utils.gen_grouped_seq(file1, pattern, n_extra_cols=0, to_shuffle=True)
    shutil.copyfile(file1, file2) #Дублируем первый файл для теста

    # Определение параметров фильтров
    bloom_size = 10 ** 7  # Размер битовой матрицы
    num_hashes = 7  # Количество хеш-функций
    sketch_width = 10 ** 5  # Ширина таблицы для Count-Min Sketch
    sketch_depth = 5  # Глубина таблицы для Count-Min Sketch
    max_keys = 10 ** 6  # Максимум уникальных ключей для точного пересечения

    # Создание Bloom-фильтра и Count-Min Sketch
    bloom_filter1 = BloomFilter(bloom_size, num_hashes)
    sketch1 = CountMinSketch(sketch_width, sketch_depth)

    # Чтение первого файла
    key_set1 = read_file_with_bloom_filter(file1, bloom_filter1, sketch1, max_keys)

    # Чтение второго файла и оценка размера JOIN
    if len(key_set1) <= max_keys:
        # Если уникальных ключей немного, используем точную оценку
        bloom_filter2 = BloomFilter(bloom_size, num_hashes)
        sketch2 = CountMinSketch(sketch_width, sketch_depth)
        key_set2 = read_file_with_bloom_filter(file2, bloom_filter2, sketch2, max_keys)
        join_keys = key_set1 & key_set2
        print(f"Точное количество пересечений: {len(join_keys)}")
    else:
        # Оценка размера JOIN с использованием Bloom-фильтра и Count-Min Sketch
        join_size = estimate_join_size(file2, bloom_filter1, sketch1)
        print(f"Оценочное количество пересечений: {join_size}")


if __name__ == '__main__':
    main()
