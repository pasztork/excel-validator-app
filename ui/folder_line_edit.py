from typing import Callable

from PyQt6.QtWidgets import QLineEdit


class FolderLineEdit(QLineEdit):
    def __init__(self, on_double_click: Callable[[], None], parent=None) -> None:
        super().__init__(parent)
        self._on_double_click = on_double_click

    def mouseDoubleClickEvent(self, event) -> None:
        self._on_double_click()
        event.accept()
