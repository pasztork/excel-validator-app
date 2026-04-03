from abc import ABC, abstractmethod

from core.validation_context import ValidationContext


class FilterBase(ABC):
    @abstractmethod
    def process(self, context: ValidationContext) -> ValidationContext:
        pass
