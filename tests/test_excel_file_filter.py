import tempfile
import unittest
from pathlib import Path

import pandas as pd

from core.excel_file_filter import ExcelFileFilter
from core.validation_context import ValidationContext


class TestExcelFileFilter(unittest.TestCase):
    def test_valid_excel_file_passes_dummy_validation(self) -> None:
        filter_ = ExcelFileFilter()

        with tempfile.TemporaryDirectory() as temp_dir:
            file_path = Path(temp_dir) / "valid.xlsx"
            pd.DataFrame({"value": [1, 2, 3]}).to_excel(file_path, index=False)
            context = ValidationContext(file_path=file_path)

            result = filter_.process(context)

            self.assertTrue(result.is_valid)
            self.assertIsNone(result.error)

    def test_empty_excel_file_fails_dummy_validation(self) -> None:
        filter_ = ExcelFileFilter()

        with tempfile.TemporaryDirectory() as temp_dir:
            file_path = Path(temp_dir) / "empty.xlsx"
            pd.DataFrame().to_excel(file_path, index=False)
            context = ValidationContext(file_path=file_path)

            result = filter_.process(context)

            self.assertFalse(result.is_valid)
            self.assertEqual(result.error, "A fájl üres")

    def test_non_excel_file_is_ignored(self) -> None:
        filter_ = ExcelFileFilter()

        with tempfile.TemporaryDirectory() as temp_dir:
            file_path = Path(temp_dir) / "notes.md"
            file_path.write_text("hello", encoding="utf-8")
            context = ValidationContext(file_path=file_path)

            result = filter_.process(context)

            self.assertTrue(result.is_valid)
            self.assertIsNone(result.error)


if __name__ == "__main__":
    unittest.main()
