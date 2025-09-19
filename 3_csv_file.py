"""
Скрипт демонструє роботу з CSV-файлами:
- Створення та запис даних.
- Читання даних, обчислення та обробка помилок.
- Додавання нового рядка.
- Керування файлом (відображення та видалення).
"""

import csv
import os

# Визначаємо шлях до файлу
script_dir = os.path.dirname(os.path.realpath(__file__))
filename = "students.csv"
file_path = os.path.join(script_dir, filename)

# Створення CSV файлу
# Дані для запису
data_to_write = [
    ["Ім'я студента", "Вік", "Оцінка"],
    ["Петро", 21, 90],
    ["Марина", 22, 85],
    ["Андрій", 20, 88],
]

# Записуємо дані у CSV-фйл
with open(file_path, 'w', newline='', encoding='utf-8') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerows(data_to_write)

print(f"Файл '{filename}' успішно створено!")

# Робота з існуючим файлом
# Читання та обчислення середньої оцінки
total_score = 0
student_count = 0

with open(file_path, 'r', newline='', encoding='utf-8') as csvfile:
    reader = csv.reader(csvfile)
    next(reader)  # Пропускаємо рядок заголовка

    for row in reader:
        try:
            score = int(row[2])  # Оцінка знаходиться в третьому стовпці (індекс 2)
            total_score += score
            student_count += 1
        except (ValueError, IndexError) as ex:
            print(f"Помилка при обробці рядка: {row}. Деталі: {ex}")

# Виведення середньої оцінки
if student_count > 0:
    average_score = total_score / student_count
    print(f"Середня оцінка студентів: {average_score:.2f}")
else:
    print("Немає даних для обчислення середньої оцінки")

# Додавання нового студента
new_student = ["Олена", 23, 95]
with open(file_path, 'a', newline='', encoding='utf-8') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(new_student)

print(f"Студент '{new_student[0]}' успішно доданий до файлу '{filename}'.")

# Відображення файлу у консоль або видалення його, за вибором користувача
print_answer = input(f"Відобразити збережений текст у файлі: '{filename}'? (відповідь має бути y або n): ").lower()
if print_answer == 'y':
    with open(file_path, 'r', encoding='utf-8') as file:
        print(f"\n{file.read()}")
elif print_answer == 'n':
    pass
else:
    print(
        f"Сталася помилка. Ваша відпоідь '{print_answer}' не є корректною. Відповідь повинна бути або 'y' або 'n'")

delete_answer = input(f"Видалити файл '{filename}'? (відповідь має бути y або n): ").lower()
if delete_answer == 'y':
    os.remove(file_path)
    print(f"Файл '{filename}' успішно видалено!")
elif delete_answer == 'n':
    pass
else:
    print(f"Сталася помилка. Ваша відпоідь '{delete_answer}' не є корректною. Відповідь повинна бути або 'y' або 'n'")
print("--- Программу завершено ---")
