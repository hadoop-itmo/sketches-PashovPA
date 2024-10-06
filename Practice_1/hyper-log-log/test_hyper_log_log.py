import random
import string
import pandas as pd
from hyper_log_log import HyperLogLog


# Функция для генерации случайной строки
def random_string(length=10):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for _ in range(length))


# Параметры для тестирования
k_values = [4, 6, 8, 10]  # Количество регистров
num_tests = 100  # Количество тестов
unique_counts = [100, 1000, 10000, 100000]  # Количество уникальных элементов

results = []

# Тестирование
for k in k_values:
    for unique_count in unique_counts:
        hll = HyperLogLog(k)
        unique_strings = {random_string() for _ in range(unique_count)}

        # Добавление строк в HyperLogLog
        for s in unique_strings:
            hll.put(s)

        # Оценка количества уникальных элементов
        estimated_count = hll.est_size()

        # Сохраняем результаты
        results.append({
            'k': k,
            'unique_count': unique_count,
            'estimated_count': estimated_count,
            'actual_count': len(unique_strings),
            'error': abs(estimated_count - len(unique_strings))
        })

# Преобразование результатов в DataFrame
results_df = pd.DataFrame(results)

# Вывод результатов
print(results_df)

# Дополнительно можно проанализировать среднюю ошибку по каждому k
error_summary = results_df.groupby('k')['error'].mean().reset_index()
print(error_summary)
