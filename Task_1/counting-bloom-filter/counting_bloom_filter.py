import mmh3
import numpy as np

class CountingBloomFilter:
    def __init__(self, k, n, cap=1):
        self.k = k  # Количество хеш-функций
        self.n = n  # Количество счетчиков
        self.cap = cap  # Количество битов для каждого счетчика
        self.size = n * cap  # Общий размер массива счетчиков
        self.counters = np.zeros((self.size,), dtype=np.uint8)  # Массив счетчиков

    def put(self, s):
        # Увеличиваем счетчики для каждого хеша
        for i in range(self.k):
            hash_value = mmh3.hash(s, i) % self.n
            self.counters[hash_value] = min(self.counters[hash_value] + 1, (1 << self.cap) - 1)

    def get(self, s):
        # Проверяем, можно ли удалить элемент
        return all(self.counters[mmh3.hash(s, i) % self.n] > 0 for i in range(self.k))

    def delete(self, s):
        # Уменьшаем счетчики для каждого хеша
        for i in range(self.k):
            hash_value = mmh3.hash(s, i) % self.n
            if self.counters[hash_value] > 0:
                self.counters[hash_value] -= 1

    def average_count(self):
        # Возвращаем сумму всех счетчиков, деленную на k
        return np.sum(self.counters) / self.k
