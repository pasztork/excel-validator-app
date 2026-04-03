from core.filter_base import FilterBase
from core.validation_context import ValidationContext

EXCEL_EXTENSIONS = {".xlsx", ".xls", ".xlsm", ".xltx", ".xltm", ".xlsb", ".md"}


class ExcelFileFilter(FilterBase):
    """Filter that marks non-Excel files as not-of-interest."""

    def process(self, context: ValidationContext) -> ValidationContext:
        """Check if the file is an Excel file and set is_of_interest accordingly."""
        file_suffix = context.file_path.suffix.lower()
        context.is_of_interest = file_suffix in EXCEL_EXTENSIONS
        return context
