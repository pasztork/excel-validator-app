from dataclasses import dataclass
from pathlib import Path


@dataclass
class ValidationContext:
    file_path: Path
    is_of_interest: bool = False
    is_valid: bool = True
    error: str = None
    data: dict = None

    def __post_init__(self):
        if self.data is None:
            self.data = {}

    def invalidate(self, error: str):
        self.is_valid = False
        self.error = error

    def flag_not_interesting(self):
        self.is_of_interest = False

    def flag_interesting(self):
        self.is_of_interest = True
