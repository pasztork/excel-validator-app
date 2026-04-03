from core.filter_base import FilterBase
from core.validation_context import ValidationContext


class Pipeline:
    def __init__(self, *filters: FilterBase):
        self.filters = filters

    def execute(self, context: ValidationContext) -> ValidationContext:
        for f in self.filters:
            context = f.process(context)
            if not context.is_of_interest or not context.is_valid:
                break
        return context
