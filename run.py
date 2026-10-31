"""Запуск генератора: python run.py <папка спецификаций> <файл тестов>.

Единственная точка входа для людей и агентов: не зависит от PYTHONPATH, от того,
из какого каталога позвали, и от того, какой Python установлен (у embeddable
дистрибутива `cwd` и `PYTHONPATH` в `sys.path` не попадают никогда).
"""
import sys
from pathlib import Path

КОРЕНЬ = Path(__file__).resolve().parent

СПРАВКА = """использование: python run.py <папка спецификаций> <файл тестов>

Порождённые тесты — не править руками: они перегенерируются.

Коды выхода:
  0 — тесты порождены
  1 — спецификация не по стандарту (файл, раздел и правило — в stderr)
  2 — неверные аргументы
"""


def _потоки_в_utf8() -> None:
    """В сообщениях генератора есть «», —, ≤, ≥; в Cp1251 их нет."""
    for поток in (sys.stdout, sys.stderr):
        try:
            поток.reconfigure(encoding="utf-8", errors="replace")
        except (AttributeError, ValueError):
            pass


def главная(аргументы: list[str]) -> int:
    if аргументы and аргументы[0] in ("-h", "--help", "-?"):
        print(СПРАВКА, end="")
        return 0
    sys.path.insert(0, str(КОРЕНЬ))
    from генератор.__main__ import главная as запуск

    return запуск(аргументы)


if __name__ == "__main__":
    _потоки_в_utf8()
    sys.exit(главная(sys.argv[1:]))
