from __future__ import annotations

from PyQt6.QtCore import QObject, QThread, pyqtSignal, pyqtSlot

from core.folder_validator import FolderValidator


class ValidationWorker(QObject):
    started = pyqtSignal(int)
    result_ready = pyqtSignal(object)
    finished = pyqtSignal()
    error_occured = pyqtSignal(str)

    @staticmethod
    def create_validation_thread(validator: FolderValidator, folder_path: str) -> tuple[QThread, ValidationWorker]:
        thread = QThread()
        worker = ValidationWorker(validator, folder_path)
        worker.moveToThread(thread)
        thread.started.connect(worker.run)
        worker.finished.connect(thread.quit)
        return thread, worker

    def __init__(self, validator: FolderValidator, folder_path: str) -> None:
        super().__init__()
        self.validator = validator
        self.folder_path = folder_path

    @pyqtSlot()
    def run(self) -> None:
        try:
            self.validator.folder_path = self.folder_path
            self.started.emit(self.validator.file_count)
            for ctx in self.validator.validate_folder():
                self.result_ready.emit(ctx)
            self.finished.emit()
        except Exception as ex:
            self.error_occured.emit(str(ex))
            self.finished.emit()
