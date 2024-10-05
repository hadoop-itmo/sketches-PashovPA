import mmh3
import numpy as np

class HyperLogLog:
    def __init__(self, k):
        self.k = k  # Количество регистров
        self.m = 1 << k  # Размер массива (2^k)
        self.alphaMM = (0.7213 / (1 + 1.079 / self.m)) * self.m * self.m  # Константа для коррекции
        self.reg = np.zeros(self.m, dtype=int)  # Массив для хранения максимальных значений

    def put(self, s):
        # Хешируем элемент
        x = mmh3.hash(s)
        # Получаем индекс регистра
        index = x & (self.m - 1)
        # Получаем число 1 перед первым 1 в хеше
        self.reg[index] = max(self.reg[index], self._rho(x))

    def _rho(self, x):
        # Считаем число нулей перед первым единичным битом
        x = x >> 32  # Берем старшую половину
        return (x | 1).bit_length()  # Количество битов до первого 1

    def est_size(self):
        # Преобразуем регистры в float и корректно возводим 2 в степень
        Z = 1.0 / np.sum([2.0 ** -float(reg) for reg in self.reg])
        E = self.alphaMM * Z

        # Корректировка для малых значений E
        if E <= (5.0 / 2.0) * self.m:
            V = np.count_nonzero(self.reg == 0)  # Количество пустых регистров
            if V > 0:
                E = self.m * np.log(self.m / V)  # Корректируем оценку
        elif E > (1 << 32):  # Если больше 2^32
            E = -(2 ** 32) * np.log(1 - E / (2 ** 32))  # Используем другую формулу

        return int(E)
