import random
import string
import pandas as pd
from counting_bloom_filter import CountingBloomFilter


# Функция для генерации случайной строки
def random_string(length=10):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(length))


# Размеры Counting Bloom-фильтра
n_values = [8, 64, 1024, 64 * 1024]
# Размеры наборов строк
set_sizes = [5, 50, 500, 5000, 5000000]
# Количество хеш-функций
k_values = [1, 2, 3, 4]

results = []

# Тестирование
for n in n_values:
    for set_size in set_sizes:
        for k in k_values:
            bloom_filter = CountingBloomFilter(k, n, cap=5)  # Указываем cap = 5 бит
            unique_strings = {random_string() for _ in range(set_size)}
            true_count = 0

            # Проверка существования строки
            for s in unique_strings:
                bloom_filter.put(s)

            # Проверка, сколько уникальных строк мы можем вернуть
            for s in unique_strings:
                if bloom_filter.get(s):
                    true_count += 1

            # Подсчет единиц в Counting Bloom-фильтре
            ones_count = bloom_filter.average_count()  # Используйте новый метод
            results.append({
                'n': n,
                'set_size': set_size,
                'k': k,
                'fp_count': true_count,
                'ones_count': ones_count
            })

# Преобразование результатов в DataFrame
results_df = pd.DataFrame(results)

# Вывод результатов
print(results_df)
