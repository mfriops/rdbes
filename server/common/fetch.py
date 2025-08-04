#!/usr/local/bin/python3
# coding: utf-8

from __future__ import annotations

# import os
# import oracledb  # Oracle driver for SQLAlchemy "oracledb" dialect
#
# from typing import Any, Dict
# from datetime import datetime
# from dotenv import load_dotenv
# from flask import Flask, abort, jsonify, request
# from sqlalchemy import Column, Float, Integer, Numeric, String, create_engine, select
from sqlalchemy import select
# from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker

# from utils.helper import to_dict, parse_int_list
from server.common.helper import to_dict

# ---------------------------------------------------------------------------
# One‑table SELECT helpers
# ---------------------------------------------------------------------------

def fetch_one(SessionLocal, model, column, value):
    """Generic helper to fetch a single record by column == value."""
    stmt = select(model).where(column == value)
    with SessionLocal() as session:
        rec = session.scalars(stmt).first()
        return to_dict(rec) if rec else None


def fetch_many(
    SessionLocal,
    model,
    column=None,
    values=None,
    *,
    where_clauses=None,
    limit=None,
    offset=None,
    order_by=None,
):
    """
    Generic helper to fetch one or many records.

    Parameters
    ----------
    model : sqlalchemy.orm.DeclarativeMeta
        The mapped class you want to query.
    column : InstrumentedAttribute | None
        A model attribute to filter on (e.g. `User.id`, `User.email`).
        Leave it None if you only want to apply `where_clauses`.
    values : Any | Iterable[Any] | None
        Value or iterable of values to match against `column`.
    where_clauses : Iterable[sqlalchemy.sql.expression.ClauseElement] | None
        Extra SQLAlchemy conditions you’d like to AND together.
    limit : int | None
    offset : int | None
    order_by : sqlalchemy.sql.expression.ClauseElement | Sequence[...]
        Order criteria (e.g. `User.created_at.desc()`).

    Returns
    -------
    list[dict]
        A list of `to_dict(record)` results (empty list if nothing matched).
    """
    stmt = select(model)

    # Primary filter (column == value or column.in_(values))
    if column is not None and values is not None:
        if isinstance(values, (list, tuple, set)):
            stmt = stmt.where(column.in_(values))
        else:
            stmt = stmt.where(column == values)

    # Optional extra predicates
    if where_clauses:
        stmt = stmt.where(and_(*where_clauses))

    # Optional sorting / paging
    if order_by is not None:
        stmt = stmt.order_by(order_by)
    if limit is not None:
        stmt = stmt.limit(limit)
    if offset is not None:
        stmt = stmt.offset(offset)

    with SessionLocal() as session:
        records = session.scalars(stmt).all()
        return [to_dict(r) for r in records]
