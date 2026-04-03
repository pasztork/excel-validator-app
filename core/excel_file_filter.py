from pathlib import Path

import pandas as pd

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
        df = pd.read_excel(file_path)
        is_empty = df.size == 0
        return (not is_empty, "A fájl üres" if is_empty else None)
