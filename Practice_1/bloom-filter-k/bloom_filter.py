"""
Задание 2

"""


import mmh3
import numpy as np

class BloomFilter:
    def __init__(self, k, n):
        self.k = k  # Количество хеш-функций
        self.size = n  # Размер битового массива
        self.bit_array = np.zeros((self.size,), dtype=bool)

    def put(self, s):
        # Используем k хеш-функций для добавления строки
        for i in range(self.k):
            hash_value = mmh3.hash(s, i) % self.size
            self.bit_array[hash_value] = True

    def get(self, s):
        # Проверяем наличие строки, используя k хеш-функций
        return all(self.bit_array[mmh3.hash(s, i) % self.size] for i in range(self.k))

    def ones_count_per_k(self):
        # Возвращаем количество единичных битов, деленное на k
        return np.sum(self.bit_array) / self.k
