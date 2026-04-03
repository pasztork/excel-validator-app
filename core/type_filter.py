from core.filter_base import FilterBase
from core.validation_context import ValidationContext


class TypeFilter(FilterBase):
    def __init__(self, supported_exts: list[str]):
        self.supported = supported_exts

    def process(self, context: ValidationContext) -> ValidationContext:
        context.is_of_interest = context.file_path.suffix.lower() in self.supported
        return context
