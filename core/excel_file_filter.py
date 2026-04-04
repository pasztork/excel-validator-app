import re

import pandas as pd

from core.filter_base import FilterBase
from core.validation_constants import ValidationConstants
from core.validation_context import ValidationContext

EXCEL_EXTENSIONS = {".xlsx", ".xls", ".xlsm", ".xltx", ".xltm", ".xlsb"}


class ExcelFileFilter(FilterBase):
    """Filter that operates on Excel files."""

    HOUR_REGEX = r"^(?:CO|LP)\(([-+]?\d+)\)$"

    def __init__(self):
        self.constants = [
            ValidationConstants("consilier școlar", 4, 21, False),
            ValidationConstants("mentor", 12, 21, True),
            ValidationConstants("profesor de limba engleza", 12, 8, True),
            ValidationConstants("profesor limbă și literatură română", 4, 40, False),
            ValidationConstants("asistent grup țintă", 4, 21, False),
            ValidationConstants("responsabil grup țintă", 12, 84, True),
            ValidationConstants("expert de consiliere și orientare ceoc", 4, 42, False),
            ValidationConstants("asistent ucp", 12, 84, True),
            ValidationConstants("manager de proiect", 12, 84, True),
        ]

    def process(self, context: ValidationContext) -> ValidationContext:
        """Check if the file is an Excel file."""
        file_suffix = context.file_path.suffix.lower()
        if file_suffix in EXCEL_EXTENSIONS:
            self._validate_excel(context)
        return context

    def _get_validation_constants(self, role: str) -> ValidationConstants | None:
        for c in self.constants:
            if c.role in role:
                return c
        return None

    def _validate_excel(self, context: ValidationContext) -> None:
        df = pd.read_excel(context.file_path, header=None)

        # Check if empty
        if df.size == 0:
            context.invalidate("A fájl üres")
            return

        # Check if role exists
        role = df.iloc[4, 4].lower()
        context.data["role"] = role
        constants = self._get_validation_constants(role)
        if constants is None:
            context.invalidate(f"Nem ismert szerepkör: {role}")
            return

        # Check if rows are okay
        total_hours_worked_idx = df.index[df.iloc[:, 0] == "Nr. de lucrate"].tolist()
        if len(total_hours_worked_idx) != 0:
            total_hours_worked_idx = total_hours_worked_idx[0]
        else:
            context.invalidate('Nem ismert a fájl sablonja, hiányzik a "Nr. de lucrate" sor')
            return

        hours = df.iloc[13:total_hours_worked_idx]

        for row_idx, row in hours.iterrows():
            # Check if hours were booked on the weekend
            if pd.isna(row.iloc[1]):
                if row.iloc[2:].notna().any():
                    context.invalidate(f"Hétvégi munkavégzés a {row_idx + 1}. sorban")
                    return
                continue

            # Check if numbers are present
            raw_values = row.iloc[[4, 5, 6, 7]].astype(str).str.strip()
            cleaned_values = raw_values.str.replace(ExcelFileFilter.HOUR_REGEX, r"\1", regex=True)
            values = pd.to_numeric(cleaned_values, errors="coerce")

            if values.isna().any():
                context.invalidate(f"Érvénytelen számérték az 5., 6., 7. vagy 8. oszlopban a {row_idx + 1}. sorban")
                return

            daily_hours = values.iloc[0] + values.iloc[1] + values.iloc[2]
            if daily_hours != values.iloc[3]:
                context.invalidate(f"Az 5., 6. és 7. oszlopok összege nem egyenlő a 8. oszloppal a {row_idx + 1}. sorban")
                return

            full_time_raw = str(row.iloc[8]).strip()
            full_time_cleaned = re.sub(ExcelFileFilter.HOUR_REGEX, r"\1", full_time_raw)
            full_time_hours = pd.to_numeric(full_time_cleaned, errors="coerce")

            if full_time_hours == 0 and constants.column_i_required:
                context.invalidate(f"A főmunkaidő hiányzik a {row_idx + 1}. sorban")
                return

            total_daily_hours = full_time_hours + daily_hours
            if total_daily_hours > constants.max_daily_hours:
                context.invalidate(f"A {row_idx + 1}. sorban {total_daily_hours} óra van elkönyvelve a megengedett {constants.max_daily_hours} helyett")
                return

        summary = df.iloc[total_hours_worked_idx : total_hours_worked_idx + 3]
        if (summary.iloc[2, [4, 5, 6, 7, 8]] != summary.iloc[:2, [4, 5, 6, 7, 8]].sum(axis=0)).any():
            context.invalidate(f"Az öszefoglaló táblázat hibás a {total_hours_worked_idx + 3}. sorban")
            return

        hours_on_project = summary.iloc[2, 4]
        if hours_on_project != constants.monthly_project_target:
            context.invalidate(f"A projekten töltőtt idő nem éri el a kívánt értéket: {constants.monthly_project_target} helyett {hours_on_project} óra lett elkönyvelve")
            return

        weekend_days_count = hours.iloc[:, 1].isna().sum().item()
        total_days = len(hours)
        max_allowed = (total_days - weekend_days_count) * constants.max_daily_hours
        actual = summary.iloc[2, [7, 8]].sum()
        if actual > max_allowed:
            context.invalidate(f"Összesen {actual} órát dolgozott, a maximálisan megengedett {max_allowed} helyett")
            return
