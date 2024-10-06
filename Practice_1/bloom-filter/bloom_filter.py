"""
Задание 1

"""


import mmh3
import numpy as np

class BloomFilter:
    def __init__(self, n):
        # Определяем размер битового массива на основе количества элементов
        self.size = n
        # Создаем битовый массив с использованием numpy
        self.bit_array = np.zeros((self.size,), dtype=bool)

    def put(self, s):
        # Генерируем хеш для строки
        hash_value = mmh3.hash(s) % self.size
        # Устанавливаем бит в 1
        self.bit_array[hash_value] = True

    def get(self, s):
        # Генерируем хеш для строки
        hash_value = mmh3.hash(s) % self.size
        # Проверяем, установлен ли бит в 1
        return self.bit_array[hash_value]

    def ones_count(self):
        # Возвращаем количество единиц в битовом массиве
        return np.sum(self.bit_array)
