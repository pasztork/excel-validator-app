from datetime import date, timedelta

from core.filter_base import FilterBase
from core.validation_context import ValidationContext


class DateFilter(FilterBase):
    ROMANIAN_MONTH_NAMES = (
        "ianuarie",
        "februarie",
        "martie",
        "aprilie",
        "mai",
        "iunie",
        "iulie",
        "august",
        "septembrie",
        "octombrie",
        "noiembrie",
        "decembrie",
    )

    @staticmethod
    def _previous_month_and_year() -> tuple[str, str, int]:
        previous_month_date = date.today().replace(day=1) - timedelta(days=1)
        month_name = DateFilter.ROMANIAN_MONTH_NAMES[previous_month_date.month - 1]
        month_number = f"{previous_month_date.month:02d}"
        return month_name, month_number, previous_month_date.year

    def process(self, context: ValidationContext) -> ValidationContext:
        previous_month_name, previous_month_number, previous_year = self._previous_month_and_year()
        normalized_path = str(context.file_path).lower()

        if ((previous_month_name in normalized_path) or (previous_month_number in normalized_path)) and (str(previous_year) in normalized_path):
            context.flag_interesting()
        else:
            context.flag_not_interesting()

        return context
