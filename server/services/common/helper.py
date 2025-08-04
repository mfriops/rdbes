#!/usr/local/bin/python3
# coding: utf-8

from typing import Any, Dict
from flask import abort
from sqlalchemy import (
    MetaData,
    Table,
    create_engine,
    text,
    Column,
    String,
    Integer,
    select,
)


# ---------------------------------------------------------------------------
# Utility: model ➜ dict
# ---------------------------------------------------------------------------

def to_dict(model) -> Dict[str, Any]:
    """Serialize a SQLAlchemy model instance into a plain ``dict``."""
    return {c.key: getattr(model, c.key) for c in model.__table__.columns}


def parse_int_list(raw: str | None, *, param_name: str) -> list[int]:
    """
    Parse ``"1,2,3" → [1, 2, 3]`` and validate.
    Raises 400 if empty or if any element is not an int.
    """
    if not raw:
        abort(400, f"Missing required query-param “{param_name}” "
                   "(use e.g. ?cruise_id=101,102)")
    try:
        return [int(x.strip()) for x in raw.split(",") if x.strip()]
    except ValueError:
        abort(400, f"Invalid integer list passed to “{param_name}”")


def parse_str_list(raw: str | None, *, param_name: str) -> list[str]:
    """
    Parse ``"1,2,3" → [1, 2, 3]`` and validate.
    Raises 400 if empty or if any element is not an int.
    """
    if not raw:
        abort(400, f"Missing required query-param “{param_name}” "
                   "(use e.g. ?cruise_id=101,102)")
    try:
        return [str(x.strip()) for x in raw.split(",") if x.strip()]
    except ValueError:
        abort(400, f"Invalid integer list passed to “{param_name}”")


def _payload_to_values(table: Table, data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Map *data* keys case-insensitively onto *table* columns.

    Unknown keys are ignored; keys matching a column name in any casing
    are kept and normalised to the real column name.
    """
    col_map = {col.name.upper(): col.name for col in table.columns}
    return {col_map[k.upper()]: v for k, v in data.items() if k.upper() in col_map}
