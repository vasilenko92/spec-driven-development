"""Запись тестов на язык проекта.

Что проверить и с какими значениями — решает генератор (см. `генерация.py`).
Как это записать — решает вывод: `Вывод` описывает контракт, `ВыводPython`
пишет `unittest`. Здесь весь текст теста, и больше нигде его нет.
"""
from __future__ import annotations

from datetime import datetime


class ВнешняяСсылка:
    """Реквизит, значением которого в тесте будет регистратор внешнего объекта."""

    def __init__(self, переменная: str):
        self.переменная = переменная


class Вывод:
    """Запись тестов: каждый метод возвращает готовые строки теста на языке проекта."""

    def значение(self, значение) -> str:
        """Литерал значения: число, строка, дата, список, запись."""
        raise NotImplementedError

    def создать(self, объект: str, элементы: list) -> str:
        """Выражение создания объекта из пар «реквизит → значение»."""
        raise NotImplementedError

    def присвоить(self, имя: str, выражение: str) -> str:
        """Строка присваивания выражения переменной теста."""
        raise NotImplementedError

    def внешний(self, переменная: str, объект: str) -> str:
        """Строка создания регистратора внешнего объекта."""
        raise NotImplementedError

    def сейчас(self, момент: datetime) -> str:
        """Строка подмены текущего момента."""
        raise NotImplementedError

    def вызов(self, переменная: str, метод: str, аргументы: list) -> str:
        """Выражение вызова метода объекта."""
        raise NotImplementedError

    def ответ(self, вызов: str, ожидание) -> str:
        """Проверка ответа метода."""
        raise NotImplementedError

    def отказ(self, вызов: str, текст: str) -> list[str]:
        """Проверка отказа: вызов отвечает ошибкой с этим текстом."""
        raise NotImplementedError

    def сбой(self, вызов: str, объект: str, метод: str, шаг: int) -> list[str]:
        """Проверка сбоя на шаге: шаг падает, метод передаёт сбой дальше."""
        raise NotImplementedError

    def прочитать(self, переменная: str, ожидание) -> str:
        """Проверка реквизитов объекта после метода."""
        raise NotImplementedError

    def вызовы(self, переменная: str, ожидание: list) -> str:
        """Проверка вызовов внешнего объекта."""
        raise NotImplementedError

    def перечисление(self, имя: str, значения: list) -> str:
        """Проверка значений перечисления и их порядка."""
        raise NotImplementedError

    def класс_есть(self, имя: str, сообщение: str) -> str:
        """Проверка, что класс объекта есть в коде."""
        raise NotImplementedError

    def файл(self, группы: dict) -> str:
        """Весь файл тестов: группы — класс → (описание, [(имя, описание, тело)])."""
        raise NotImplementedError
