from pathlib import Path

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QBrush, QColor
from PyQt6.QtWidgets import (
    QFileDialog,
    QFrame,
    QHBoxLayout,
    QLabel,
    QMainWindow,
    QMessageBox,
    QProgressBar,
    QPushButton,
    QTableWidget,
    QTableWidgetItem,
    QVBoxLayout,
    QWidget,
)

# import ui.resources_rc  # noqa: F401
from core.folder_validator import FolderValidator
from core.validation_context import ValidationContext
from ui.folder_line_edit import FolderLineEdit
from ui.validation_worker import ValidationWorker


class MainWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("Excel ellenőrző")
        # self.setWindowIcon(QIcon(":/icon.png"))
        self.resize(1000, 600)

        self.validator = FolderValidator()
        self.validation_thread = None
        self.validation_worker = None

        self._build_ui()

    def closeEvent(self, event) -> None:
        if self.validation_thread is not None:
            self.validation_thread.quit()
            self.validation_thread.wait()
        event.accept()

    def _build_ui(self) -> None:
        root = QWidget(self)
        self.setCentralWidget(root)

        main_layout = QHBoxLayout(root)
        main_layout.setContentsMargins(16, 16, 16, 16)
        main_layout.setSpacing(16)

        left_panel = self._build_left_panel()
        right_panel = self._build_right_panel()

        main_layout.addWidget(left_panel, 1)
        main_layout.addWidget(right_panel, 2)

    def _build_left_panel(self) -> QFrame:
        panel = QFrame(self)
        panel.setFrameShape(QFrame.Shape.StyledPanel)

        layout = QVBoxLayout(panel)
        layout.setSpacing(10)

        title = QLabel("Beállítások", panel)
        title.setStyleSheet("font-size: 16px; font-weight: 600;")

        self.folder_input = FolderLineEdit(self._choose_folder, panel)
        self.folder_input.setPlaceholderText("Válassz ki egy mappát...")
        self.folder_input.setReadOnly(True)

        browse_button = QPushButton("Mappa választás", panel)
        browse_button.clicked.connect(self._choose_folder)

        run_button = QPushButton("Ellenőrzés", panel)
        run_button.clicked.connect(self._run_validation)

        self.progress_bar = QProgressBar(panel)
        self.progress_bar.setRange(0, 1)
        self.progress_bar.setValue(0)
        self.progress_bar.setVisible(False)

        layout.addWidget(title)
        layout.addWidget(self.folder_input)
        layout.addWidget(browse_button)
        layout.addWidget(run_button)
        layout.addWidget(self.progress_bar)
        layout.addStretch(1)

        return panel

    def _build_right_panel(self) -> QFrame:
        panel = QFrame(self)
        panel.setFrameShape(QFrame.Shape.StyledPanel)

        layout = QVBoxLayout(panel)
        layout.setSpacing(10)

        title = QLabel("Ellenőrzés eredményei", panel)
        title.setStyleSheet("font-size: 16px; font-weight: 600;")

        self.results_table = QTableWidget(panel)
        self.results_table.setColumnCount(3)
        self.results_table.setHorizontalHeaderLabels(["Fájl", "Státusz", "Üzenet"])
        self.results_table.horizontalHeader().setStretchLastSection(True)
        self.results_table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.results_table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)

        self.results_table.setStyleSheet("""
            QTableWidget::item:hover {
                background-color: rgba(180, 180, 0, 255);
            }
        """)

        layout.addWidget(title)
        layout.addWidget(self.results_table)

        return panel

    def _choose_folder(self) -> None:
        selected = QFileDialog.getExistingDirectory(self, "Mappa választás")
        if selected:
            self.folder_input.setText(selected)

    def _run_validation(self) -> None:
        folder = self.folder_input.text().strip()
        if not folder:
            QMessageBox.warning(self, "Nem választottál ki mappát", "Válassz ki egy mappát előbb")
            return

        folder_path = Path(folder)
        if not folder_path.exists() or not folder_path.is_dir():
            QMessageBox.critical(self, "Hibás mappa", "A kiválasztott mappát nem nyitható meg")
            return

        self._start_validation(folder)

    def _start_validation(self, folder: str) -> None:
        if self.validation_thread is not None:
            return

        self.results_table.setRowCount(0)
        self.progress_bar.setVisible(True)
        self.progress_bar.setRange(0, 0)
        self.progress_bar.setValue(0)

        self.validation_thread, self.validation_worker = ValidationWorker.create_validation_thread(self.validator, folder)
        self.validation_worker.started.connect(self._on_validation_started)
        self.validation_worker.result_ready.connect(self._on_validation_result)
        self.validation_worker.error_occured.connect(self._on_validation_error)
        self.validation_worker.finished.connect(self._on_validation_finished)

        self.validation_thread.finished.connect(self.validation_worker.deleteLater)
        self.validation_thread.finished.connect(self.validation_thread.deleteLater)
        self.validation_thread.finished.connect(self._clear_validation_thread)

        self.validation_thread.start()

    def _append_result(self, result: ValidationContext, root_folder: Path) -> None:
        try:
            relative_or_name = str(result.file_path.relative_to(root_folder))
        except ValueError:
            relative_or_name = result.file_path.name

        status = "OK" if result.is_valid else "Hibás"

        row = self.results_table.rowCount()
        self.results_table.insertRow(row)

        file_item = QTableWidgetItem(relative_or_name)
        status_item = QTableWidgetItem(status)
        message_item = QTableWidgetItem(result.error)

        status_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)

        bg_color = QColor(220, 255, 220) if result.is_valid else QColor(255, 220, 220)
        bg_brush = QBrush(bg_color)
        text_brush = QBrush(QColor(33, 33, 33))
        for item in [file_item, status_item, message_item]:
            item.setBackground(bg_brush)
            item.setForeground(text_brush)

        self.results_table.setItem(row, 0, file_item)
        self.results_table.setItem(row, 1, status_item)
        self.results_table.setItem(row, 2, message_item)

    def _on_validation_started(self, total_files: int) -> None:
        self.progress_bar.setRange(0, total_files if total_files > 0 else 1)
        self.progress_bar.setValue(0)

    def _on_validation_result(self, result: ValidationContext) -> None:
        self.progress_bar.setValue(self.progress_bar.value() + 1)

        if result.is_of_interest:
            root_folder = Path(self.folder_input.text().strip())
            self._append_result(result, root_folder)

    def _on_validation_error(self, message: str) -> None:
        QMessageBox.critical(self, "Ellenőrzési hiba", message)

    def _on_validation_finished(self) -> None:
        if self.progress_bar.maximum() > 0:
            self.progress_bar.setValue(self.progress_bar.maximum())
        self.progress_bar.setVisible(False)

    def _clear_validation_thread(self) -> None:
        self.validation_thread = None
        self.validation_worker = None
