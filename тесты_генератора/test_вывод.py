"""Проверки генератора: вывод не изменился, лаунчер отвечает по контракту.

Это сетка для правок генератора: пока она зелёная, шов не изменил ни одного
символа в порождённых тестах, а точка входа работает из любого каталога.
"""
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

КОРЕНЬ = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(КОРЕНЬ))

from генератор.вывод.python import ВыводPython          # noqa: E402
from генератор.генерация import Генератор               # noqa: E402
from генератор.парсер import прочитать_спецификации      # noqa: E402

ЭТАЛОН = КОРЕНЬ / "пример" / "tests" / "test_по_спецификации.py"


class ВыводНеИзменился(unittest.TestCase):
    def test_пример_совпадает_с_закоммиченным(self):
        объекты = прочитать_спецификации(КОРЕНЬ / "пример" / "спеки")
        self.assertEqual(ЭТАЛОН.read_text(encoding="utf-8"), Генератор(объекты).все() + "\n")

    def test_вывод_по_умолчанию_это_python(self):
        объекты = прочитать_спецификации(КОРЕНЬ / "пример" / "спеки")
        self.assertEqual(Генератор(объекты).все(), Генератор(объекты, ВыводPython()).все())


class Запуск(unittest.TestCase):
    """run.py — единственная точка входа; коды выхода нужны агенту, а не человеку."""

    def _run(self, *аргументы: str) -> subprocess.CompletedProcess:
        return subprocess.run([sys.executable, str(КОРЕНЬ / "run.py"), *аргументы],
                              cwd=КОРЕНЬ, capture_output=True)

    def test_справка_это_ноль(self):
        итог = self._run("--help")
        self.assertEqual(0, итог.returncode)
        self.assertIn("использование", итог.stdout.decode("utf-8"))

    def test_без_аргументов_это_два(self):
        self.assertEqual(2, self._run().returncode)

    def test_прогон_во_временный_файл_совпадает_с_эталоном(self):
        with tempfile.TemporaryDirectory() as папка:
            выход = Path(папка) / "test_пример.py"
            итог = self._run("пример/спеки", str(выход))
            self.assertEqual(0, итог.returncode, итог.stderr.decode("utf-8", "replace"))
            self.assertEqual(ЭТАЛОН.read_text(encoding="utf-8"), выход.read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()
