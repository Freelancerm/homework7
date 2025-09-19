import json
import os

# Інформація для запису
data = [
    {"назва": "Книга 1", "автор": "Автор 1", "рік": 2015, "наявність": True},
    {"назва": "Книга 2", "автор": "Автор 2", "рік": 2018, "наявність": False}
]
# Визначаємо ім'я файлу
filename = "books.json"
file_path = os.path.join(os.getcwd(), filename)

print(f"Створення файлу '{filename}' з початковими даними....")
with open(file_path, "w", encoding="utf-8") as file:
    json.dump(data, file, indent=4, ensure_ascii=False)
print("Файл успішно створено.\n")


print("Завантаження файлу та виведення книг в наявності:")
if os.path.exists(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        books_data = json.load(file)
        available_books = [book for book in books_data if book.get("наявність") is True]

        if available_books:
            print("--- Книги, які в наявності: ---")
            for book in available_books:
                print(f"Назва: {book['назва']}, Автор: {book['автор']}, Рік: {book['рік']}")
            else:
                print(f"Помилка: файл '{filename}' не знайдено.")

# Додавання нової книги та оновлення файлу
print("\n--- Додавання нової книги ---")
new_book = {
    "назва": "Нова Книга",
    "автор": "Новий Автор",
    "рік": 2023,
    "наявність": True
}

books_data.append(new_book)
print(f"Книгу '{new_book['назва']}' додано до списку.")

with open(file_path, "w", encoding="utf-8") as file:
    json.dump(books_data, file, indent=4, ensure_ascii=False)
print("Файл успішно оновлено.\n")

# Перевірка оновленого списку
print("--- Оновлений список доступних книг: ---")
updated_available_books = [book for book in books_data if book.get("наявність") is True]
for book in updated_available_books:
    print(f"Назва: {book['назва']}, Автор: {book['автор']}, Рік: {book['рік']}")

# Можливість видалення файлу
while True:
    delete_answer = input(f"Видалити файл '{filename}'? (відповідь має бути 'y' або 'n'").lower()
    if delete_answer == "y":
        if os.path.exists(file_path):
            os.remove(file_path)
            print(f"Файл '{filename}' успішно видалено!")
        else:
            print(f"Помилка: Файл '{filename}' вже був видалений або не існує.")
        break
    elif delete_answer == "n":
        print(f"Файл '{filename}' не було видалено.")
        break
    else:
        print(f"Помилка: Ваша відповідь '{delete_answer}' не є коректною. Відповідь повинна бути 'y' або 'n'")

    print("Програму завершено")