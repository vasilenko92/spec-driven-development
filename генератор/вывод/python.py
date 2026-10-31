"""Запись тестов на `unittest`: та же, что была до появления вывода."""
from __future__ import annotations

from datetime import datetime

from . import ВнешняяСсылка, Вывод


class ВыводPython(Вывод):
    """Тесты на `unittest`."""

    def значение(self, значение) -> str:
        if isinstance(значение, datetime):
            return f"datetime({значение.year}, {значение.month}, {значение.day}, {значение.hour}, {значение.minute})"
        if isinstance(значение, list):
            return "[" + ", ".join(self.значение(э) for э in значение) + "]"
        if isinstance(значение, tuple):
            return "(" + ", ".join(self.значение(э) for э in значение) + ("," if len(значение) == 1 else "") + ")"
        if isinstance(значение, dict):
            return "{" + ", ".join(f"{self.значение(к)}: {self.значение(з)}" for к, з in значение.items()) + "}"
        return repr(значение)

    def создать(self, объект: str, элементы: list) -> str:
        части = [f"{self.значение(ключ)}: {self._элемент(значение)}" for ключ, значение in элементы]
        return f"тест_обвязка.создать({self.значение(объект)}, {{{', '.join(части)}}})"

    def _элемент(self, значение) -> str:
        if isinstance(значение, tuple):        # вложенный объект: (имя, элементы)
            return self.создать(*значение)
        if isinstance(значение, ВнешняяСсылка):
            return значение.переменная
        return self.значение(значение)

    def присвоить(self, имя: str, выражение: str) -> str:
        return f"{имя} = {выражение}"

    def внешний(self, переменная: str, объект: str) -> str:
        return f"{переменная} = тест_обвязка.внешний({self.значение(объект)})"

    def сейчас(self, момент: datetime) -> str:
        return f"тест_обвязка.сейчас({self.значение(момент)})"

    def вызов(self, переменная: str, метод: str, аргументы: list) -> str:
        return f"{переменная}.{метод}({', '.join(self.значение(а) for а in аргументы)})"

    def ответ(self, вызов: str, ожидание) -> str:
        return f"self.assertEqual({вызов}, {self.значение(ожидание)})"

    def отказ(self, вызов: str, текст: str) -> list[str]:
        return [
            "with self.assertRaises(Exception) as ошибка:",
            f"    {вызов}",
            f"self.assertIn({self.значение(текст)}, str(ошибка.exception))",
        ]

    def сбой(self, вызов: str, объект: str, метод: str, шаг: int) -> list[str]:
        return [
            f"with тест_обвязка.сбой_на_шаге({self.значение(объект)}, {self.значение(метод)}, {шаг}):",
            "    with self.assertRaises(тест_обвязка.Сбой):",
            f"        {вызов}",
        ]

    def прочитать(self, переменная: str, ожидание) -> str:
        return f"self.assertEqual(тест_обвязка.прочитать({переменная}), {self.значение(ожидание)})"

    def вызовы(self, переменная: str, ожидание: list) -> str:
        return f"self.assertEqual({переменная}.вызовы, {self.значение(ожидание)})"

    def перечисление(self, имя: str, значения: list) -> str:
        return f"self.assertEqual(тест_обвязка.значения_перечисления({self.значение(имя)}), {self.значение(значения)})"

    def класс_есть(self, имя: str, сообщение: str) -> str:
        return f"self.assertIsNotNone(тест_обвязка.класс({self.значение(имя)}), {self.значение(сообщение)})"

    def файл(self, группы: dict) -> str:
        строки = [
            "# Сгенерировано по спецификации: не править руками, перегенерировать.",
            "import unittest",
            "from datetime import datetime",
            "",
            "from tests import тест_обвязка",
        ]
        for класс, (описание_группы, тесты) in группы.items():
            while строки[-1] == "":
                строки.pop()
            строки += ["", "", f"class {класс}(unittest.TestCase):"]
            строки += _документация([описание_группы], "    ")
            строки.append("")
            for имя, описание, тело in тесты:
                строки.append(f"    def {имя}(self):")
                строки += _документация(описание, "        ")
                строки += ["        " + с for с in тело]
                строки.append("")
        return "\n".join(строки).rstrip()


def _документация(строки: list[str], отступ: str) -> list[str]:
    """Строка документации Python: её первую строку печатает unittest -v рядом с именем теста."""
    чистые = [с.replace("\\", "\\\\").replace(chr(34) * 3, chr(39) * 3) for с in строки]
    if len(чистые) == 1:
        return [f'{отступ}"""{чистые[0]}"""']
    return [f'{отступ}"""{чистые[0]}', *[отступ + с for с in чистые[1:]], f'{отступ}"""']
