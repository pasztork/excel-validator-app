from datetime import date, datetime, timedelta
from pathlib import Path

from core.filter_base import FilterBase
from core.validation_context import ValidationContext


class DateFilter(FilterBase):
    @staticmethod
    def _previous_month_and_year() -> tuple[int, int]:
        previous_month_date = date.today().replace(day=1) - timedelta(days=1)
        return previous_month_date.month, previous_month_date.year

    def process(self, context: ValidationContext) -> ValidationContext:
        previous_month, previous_year = DateFilter._previous_month_and_year()
        file_stat = Path(context.file_path).stat()
        created_timestamp = getattr(file_stat, "st_birthtime", file_stat.st_ctime)
        created_date = datetime.fromtimestamp(created_timestamp).date()
        modified_date = datetime.fromtimestamp(file_stat.st_mtime).date()

        created_last_month = created_date.month == previous_month and created_date.year == previous_year
        modified_last_month = modified_date.month == previous_month and modified_date.year == previous_year
        modified_this_month = modified_date.month == date.today().month and modified_date.year == date.today().year

        if created_last_month or modified_last_month or modified_this_month:
            context.flag_interesting()
        else:
            context.flag_not_interesting()

        return context
