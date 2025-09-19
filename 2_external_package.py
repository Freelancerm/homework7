import requests
import os

# Задаємо URL для завантаження
url = "https://uk.wikipedia.org/wiki/Python"

# Прописуємо User-Agent для емуляції реального браузеру, щоб обійти обмеження по скачуванню інформації
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
}

# Визначаємо абсолютний шлях до директорії, де знаходиться скрипт
script_dir = os.path.dirname(os.path.realpath(__file__))

# Назва файлу для збереження
filename = "python_wiki.txt"
file_path = os.path.join(script_dir, filename)

try:
    # Відправлємо GET запит
    response = requests.get(url, headers=headers)

    # Перевіряємо чи запит успішний
    if response.status_code == 200:
        print(f"Сторінку успішно завантажено! Статус код: {response.status_code}")

        # Відкриваємо файл для запису
        with open(file_path, 'w', encoding='utf-8') as file:
            # Записуємо вміст сторінки в файл
            file.write(response.text)

        print(f"Вміст сторінки успішно записано у файлі '{filename}'")

        print_answer = input(f"Відобразити збережений текст у файлі: '{filename}'? (відповідь має бути y або n): ").lower()
        if print_answer == 'y':
            with open(file_path, 'r', encoding='utf-8') as file:
                print(file.read())
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
            print(
                f"Сталася помилка. Ваша відпоідь '{delete_answer}' не є корректною. Відповідь повинна бути або 'y' або 'n'")

    else:
        print(f"Не вдалося завантажити сторінку. Статус код: {response.status_code}")

except requests.exceptions.RequestException as exception:
    print(f"Сталася помилка. Детальний опис : {exception}")
print("--- Программу завершено ---")
