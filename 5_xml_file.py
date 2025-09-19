"""
Скрипт для створення та роботи з XML-файлами,
що демонструє читання, оновлення та запис даних.
"""
import xml.etree.ElementTree as ET
import os


def create_xml_file():
    """Створює XML-файл з інформацією про продукти."""
    root = ET.Element('products')

    product1 = ET.SubElement(root, 'product')
    name1 = ET.SubElement(product1, 'name')
    name1.text = 'Молоко'
    price1 = ET.SubElement(product1, 'price')
    price1.text = '25'
    quantity1 = ET.SubElement(product1, 'quantity')
    quantity1.text = '50'

    product2 = ET.SubElement(root, 'product')
    name2 = ET.SubElement(product2, 'name')
    name2.text = 'Хліб'
    price2 = ET.SubElement(product2, 'price')
    price2.text = '10'
    quantity2 = ET.SubElement(product2, 'quantity')
    quantity2.text = '100'

    tree = ET.ElementTree(root)
    tree.write('products.xml', encoding='utf-8', xml_declaration=True)
    print("Файл 'products.xml' успішно створено.")


def read_and_update_xml():
    """Читає, оновлює та зберігає XML-файл."""
    try:
        tree = ET.parse('products.xml')
        root = tree.getroot()

        print("\nСписок продуктів та їх кількість:")
        for product in root.findall('product'):
            name = product.find('name').text
            quantity = product.find('quantity').text
            print(f"Назва продукту: {name}, Кількість: {quantity}")

            # Зміна кількості хліба
            if name == 'Хліб':
                new_quantity = 80
                product.find('quantity').text = str(new_quantity)
                print(f"Оновлено кількість для '{name}' на {new_quantity}.")

        tree.write('products.xml', encoding='utf-8', xml_declaration=True)
        print("\nЗміни успішно збережено у файл 'products.xml'.")

    except FileNotFoundError:
        print("Помилка: Файл 'products.xml' не знайдено.")
    except Exception as ex:
        print(f"Сталася помилка: {ex}")


if __name__ == '__main__':
    create_xml_file()
    read_and_update_xml()

# Можливість видалення файлу
while True:
    delete_answer = input(f"Видалити файл 'products.xml'? (відповідь має бути 'y' або 'n'").lower()
    if delete_answer == "y":
        if os.path.exists('products.xml'):
            os.remove('products.xml')
            print(f"Файл 'products.xml' успішно видалено!")
        else:
            print(f"Помилка: Файл 'products.xml' вже був видалений або не існує.")
        break
    elif delete_answer == "n":
        print(f"Файл 'products.xml' не було видалено.")
        break
    else:
        print(f"Помилка: Ваша відповідь '{delete_answer}' не є коректною. Відповідь повинна бути 'y' або 'n' ")

    print("Програму завершено")
