import signal
import sys

from PyQt6.QtCore import QTimer
from PyQt6.QtWidgets import QApplication

from ui.main_window import MainWindow


def main() -> None:
    app = QApplication([])
    signal.signal(signal.SIGINT, lambda *_: app.quit())

    # Keep the event loop responsive to Python signal handlers.
    timer = QTimer()
    timer.timeout.connect(lambda: None)
    timer.start(100)

    window = MainWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
