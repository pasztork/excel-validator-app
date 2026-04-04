from dataclasses import dataclass


@dataclass
class ValidationConstants:
    role: str
    max_daily_hours: int
    monthly_project_target: int
    column_i_required: bool
