from pathlib import Path

from core.filter_base import FilterBase
from core.validation_context import ValidationContext

EXCEL_EXTENSIONS = {".xlsx", ".xls", ".xlsm", ".xltx", ".xltm", ".xlsb"}


class ExcelFileFilter(FilterBase):
    """Filter that operates on Excel files."""

    def process(self, context: ValidationContext) -> ValidationContext:
        """Check if the file is an Excel file."""
        file_suffix = context.file_path.suffix.lower()
        if file_suffix in EXCEL_EXTENSIONS:
            context.is_valid, context.error = self._validate_excel(context.file_path)
        return context

    def _validate_excel(self, file_path: Path) -> tuple[bool, str | None]:
        if file_path.stat().st_size > 0:
            return (True, None)
        return (False, "A fájl üres")
