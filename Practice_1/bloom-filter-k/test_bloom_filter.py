import random
import string
import pandas as pd
from bloom_filter import BloomFilter


# Функция для генерации случайной строки
def random_string(length=10):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(length))


# Размеры Bloom-фильтра
bf_sizes = [8, 64, 1024, 64 * 1024, 16 * 1024 * 1024]
# Размеры наборов строк
set_sizes = [5, 50, 500, 5000, 5000000]
# Количество хеш-функций
k_values = [1, 2, 3, 4]

results = []

# Тестирование
for bf_size in bf_sizes:
    for set_size in set_sizes:
        for k in k_values:
            bloom_filter = BloomFilter(k, bf_size)
            unique_strings = {random_string() for _ in range(set_size)}
            true_count = 0

            # Проверка существования строки
            for s in unique_strings:
                if bloom_filter.get(s):
                    true_count += 1
                bloom_filter.put(s)

            # Подсчет единиц в Bloom-фильтре
            ones_count = bloom_filter.ones_count_per_k()  # Используйте новый метод
            results.append({
                'bf_size': bf_size,
                'set_size': set_size,
                'k': k,
                'fp_count': true_count,
                'ones_count': ones_count
            })

# Преобразование результатов в DataFrame
results_df = pd.DataFrame(results)

# Вывод результатов
print(results_df)
