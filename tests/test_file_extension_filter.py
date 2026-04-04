import unittest
from pathlib import Path

from core.file_extension_filter import FileExtensionFilter
from core.validation_context import ValidationContext


class TestFileExtensionFilter(unittest.TestCase):
    def test_marks_supported_extension_as_interesting(self) -> None:
        filter_ = FileExtensionFilter([".xlsx", ".xlsm"])
        context = ValidationContext(file_path=Path("report.xlsx"))

        result = filter_.process(context)

        self.assertTrue(result.is_of_interest)

    def test_marks_unsupported_extension_as_not_interesting(self) -> None:
        filter_ = FileExtensionFilter([".xlsx"])
        context = ValidationContext(file_path=Path("notes.md"))

        result = filter_.process(context)

        self.assertFalse(result.is_of_interest)


if __name__ == "__main__":
    unittest.main()
