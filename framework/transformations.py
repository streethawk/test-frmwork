from __future__ import annotations

from datetime import datetime
from decimal import Decimal
from typing import Callable


def _strip(value: str) -> str:
    return value.strip()


def _upper(value: str) -> str:
    return value.upper()


def _to_decimal(value: str) -> Decimal:
    return Decimal(value)


def _date_yyyymmdd(value: str) -> datetime:
    return datetime.strptime(value, "%Y%m%d")


TRANSFORMATIONS: dict[str, Callable[[str], object]] = {
    "strip": _strip,
    "upper": _upper,
    "to_decimal": _to_decimal,
    "date_yyyymmdd": _date_yyyymmdd,
}


def apply_transformation(value: str, transformation: str | None) -> object:
    if transformation is None:
        return value
    if transformation not in TRANSFORMATIONS:
        raise KeyError(f"Unknown transformation: {transformation}")
    return TRANSFORMATIONS[transformation](value)
