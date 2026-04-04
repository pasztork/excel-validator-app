from dataclasses import dataclass, field


@dataclass(frozen=True)
class ValidationConstants:
    max_daily_hours: int
    monthly_project_target: int
    column_i_required: bool
    possible_role_names: tuple[str, ...] = field(default_factory=tuple)
