from pathlib import Path
from typing import Iterator

from core.excel_file_filter import ExcelFileFilter
from core.pipeline import Pipeline
from core.validation_context import ValidationContext


class FolderValidator:
    """Validator for scanning and validating files in a folder."""

    def __init__(self):
        self.folder_path = None
        self.pipe = Pipeline(ExcelFileFilter())

    @property
    def file_count(self) -> int:
        return len(self._iter_files())

    def validate_folder(self) -> Iterator[ValidationContext]:
        """Yield validation contexts and skip non-interest results."""

        for path in self._iter_files():
            yield self._validate_file(path)

    def _iter_files(self) -> list[Path]:
        root = Path(self.folder_path)
        if not root.exists() or not root.is_dir():
            return []

        return [path for path in sorted(root.rglob("*")) if path.is_file()]

    def _validate_file(self, file_path: Path) -> ValidationContext:
        return self.pipe.execute(ValidationContext(file_path=file_path))
