""" Модуль, що містить математичні функції """

import math


def factorial(number):
    """
    Функція для обчислення факторіалу числа, та повернення його результату

    :param number: Число, для якого обчислюється факторіал.
    :return: Факторіал числа
    """
    factorial_result = math.factorial(number)
    return factorial_result


def gcd(num1, num2):
    """
    Функція, для знаходження найбільшого спільного дільника двох чисел

    :param num1: Перше число.
    :param num2: Друге число.
    :return: Найбільший спільний дільник.
    """
    result = math.gcd(num1, num2)
    return result
