from dataclasses import dataclass
from pathlib import Path


@dataclass
class ValidationContext:
    file_path: Path
    is_of_interest: bool = True
    is_valid: bool = True
    error: str = None
    data: dict = None

    def __post_init__(self):
        if self.data is None:
            self.data = {}
