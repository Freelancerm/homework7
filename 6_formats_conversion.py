import csv
import json
import xml.etree.ElementTree as ET
import os
from abc import ABC, abstractmethod


class Converter(ABC):
    """ Абстрактний базовий клас для конвертерів. """

    @abstractmethod
    def convert_to_json(self, input_path: str, output_path: str):
        pass

    @abstractmethod
    def convert_from_json(self, input_path: str, output_path: str):
        pass


class CSVtoJSON(Converter):
    """ Конвертує CSV-файл до JSON та навпаки """

    def convert_to_json(self, input_path: str, output_path: str):
        """ Конвертує CSV до JSON """
        data = []
        try:
            with open(input_path, 'r', newline='', encoding='utf-8') as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:
                    data.append(row)
            with open(output_path, 'w', newline='', encoding='utf-8') as jsonfile:
                json.dump(data, jsonfile, ensure_ascii=False, indent=4)
            print(f"Успішно конвертовано {input_path} до {output_path}")
        except FileNotFoundError:
            print(f"Помилка: Файл {input_path} не знайдено")
        except Exception as ex:
            print(f"Сталася помилка при конвертації CSV до JSON: {ex}")

    def convert_from_json(self, input_path: str, output_path: str):
        """ Конвертує JSON до CSV. """
        try:
            with open(input_path, 'r', encoding='utf-8') as jsonfile:
                data = json.load(jsonfile)

            if not data:
                print("Помилка: JSON файл порожній.")
                return

            if not isinstance(data, list) or not all(isinstance(item, dict) for item in data):
                print("Помилка: Очікується список словників.")
                return

            keys = data[0].keys()
            with open(output_path, 'w', newline='', encoding='utf-8') as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=keys)
                writer.writeheader()
                writer.writerows(data)
            print(f"Успішно конвертовано {input_path} до {output_path}.")
        except FileNotFoundError:
            print(f"Помилка: Файл {input_path} не знайдено.")
        except Exception as ex:
            print(f"Сталася помилка при конвертації JSON до CSV: {ex}")


class XMLConverter(Converter):
    """ Конвертує XML-файл до JSON та навпаки. """

    def convert_to_json(self, input_path: str, output_path: str):
        """ Конвертує XML до JSON """
        try:
            tree = ET.parse(input_path)
            root = tree.getroot()
            data = self._xml_to_dict(root)

            with open(output_path, 'w', encoding='utf-8') as jsonfile:
                json.dump(data, jsonfile, indent=4)
            print(f"Успішно конвертовано {input_path} до {output_path}.")
        except FileNotFoundError:
            print(f"Помилка: Файл {input_path} не знайдено.")
        except ET.ParseError as ex:
            print(f"Помилка парсингу XML: {ex}")
        except Exception as ex:
            print(f"Сталася помилка при конвертації XML до JSON: {ex}")

    def convert_from_json(self, input_path: str, output_path: str):
        """ Конвертує JSON до XML """
        try:
            with open(input_path, 'r', encoding='utf-8') as jsonfile:
                data = json.load(jsonfile)

            if not data:
                print("Помилка: JSON-файл порожній.")
                return

            root_name = list(data.keys())[0] if isinstance(data, dict) and data else "root"
            root = ET.Element(root_name)
            self._dict_to_xml(data.get(root_name, data), root)

            tree = ET.ElementTree(root)
            tree.write(output_path, encoding='utf-8', xml_declaration=True)
            print(f"Успішно конвертовано {input_path} до {output_path}")
        except FileNotFoundError:
            print(f"Помилка: Файл {input_path} не знайдено.")
        except Exception as ex:
            print(f"Сталася помилка при конвертації JSON до XML: {ex}")

    def _xml_to_dict(self, element):
        """ Допоміжна функція для рекурсивного перетворення XML-клкментів у словник """
        result = {}
        children = list(element)

        if not children:
            return {element.tag: element.text.strip() if element.text else None}
        else:
            result[element.tag] = []
            for child in children:
                child_dict = self._xml_to_dict(child)
                result[element.tag].append(child_dict)
            return result

    def _dict_to_xml(self, data, parent_element):
        """ Допоміжна функція для рекурсивного перетворення словника в XML-елементи. """
        if isinstance(data, dict):
            for key, value in data.items():
                element = ET.SubElement(parent_element, key)
                self._dict_to_xml(value, element)
        elif isinstance(data, list):
            for item in data:
                element = ET.SubElement(parent_element, parent_element.tag[:-1])
                self._dict_to_xml(item, element)
        else:
            parent_element.text = str(data)


def _create_test_files():
    """ Створює тестові CSV та XML файли. """
    print("Створення текстових файлів....")
    # CSv файл
    with open('users.csv', 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['name', 'age', 'city'])
        writer.writerow(['Alice', '30', 'New York'])
        writer.writerow(['Bob', '25', 'London'])

        # XML файл
    with open('users.xml', 'w', encoding='utf-8') as f:
        f.write(
            '<users><user><name>Charlie</name><age>45</age></user><user><name>Dana</name><age>35</age></user></users>')

        # JSON файл для зворотного перетворення
    with open('users_from_xml.json', 'w', encoding='utf-8') as f:
        json.dump({"users": [{"user": {"name": "Eve", "age": 28}}, {"user": {"name": "Frank", "age": 42}}]}, f,
                  indent=4)
    print("Тестові файли успішно створено.")


def _cleanup_test_files():
    """ Видаляє усі створені тестові файли. """
    print("\n Видалення тестових файлів....")
    files_to_remove = ['users.csv', 'users.json', 'users.xml', 'users_back.csv', 'users_from_xml.json',
                       'users_to_xml.xml']
    for file_path in files_to_remove:
        if os.path.exists(file_path):
            os.remove(file_path)
            print(f"Видалено: {file_path}")
        else:
            print(f"Файл {file_path} не знайдено, пропущено.")
    print("Очищення завершено")


def main():
    _create_test_files()

    # Демонстрація CSV конвертера
    print("\n--- Демонстрація CSV конвертації ---")
    csv_converter = CSVtoJSON()
    csv_converter.convert_to_json('users.csv', 'users.json')
    csv_converter.convert_from_json('users.json', 'users_back.csv')

    # Демонстрація XML конвертера
    print("\n--- Демонстрація XML конвертації ---")
    xml_converter = XMLConverter()
    xml_converter.convert_to_json('users.xml', 'users.json')
    xml_converter.convert_from_json('users_from_xml.json', 'users_to_xml.xml')

    # Запит на видалення файлів
    while True:
        choice = input("\nБажаєте видалити згенеровані файли? (Y/N): ").strip().upper()
        if choice == 'Y':
            _cleanup_test_files()
            break
        elif choice == 'N':
            print("Файли залишено. Робота завершена.")
            break
        else:
            print("Будь ласка, введіть 'Y' або 'N'.")


if __name__ == '__main__':
    main()
