#!/usr/local/bin/python3
# coding: utf-8

import os
import oracledb
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

# ---------------------------------------------------------------------------
# Environment & SQLAlchemy bootstrap
# ---------------------------------------------------------------------------

def get_session_local() -> sessionmaker[Session]:
    """
    Initializes and returns a SQLAlchemy sessionmaker for Oracle database.

    Returns:
        SessionLocal (sessionmaker): Configured SQLAlchemy session factory.
    Raises:
        RuntimeError: If required environment variables are missing.
    """
    # Load environment variables from .env file
    load_dotenv()

    # Define Oracle DB connection arguments
    print(os.getenv("DB_RDBES_USR"))
    print(os.getenv("DB_RDBES_PWD"))
    print(os.getenv("DB_RDBES_DSN"))

    CONNECT_ARGS = {
        "user": os.getenv("DB_RDBES_USR"),
        "password": os.getenv("DB_RDBES_PWD"),
        "dsn": os.getenv("DB_RDBES_DSN"),
        "cclass": "MYAPP",  # client class visible in v$session
        "purity": oracledb.ATTR_PURITY_SELF,
    }

    # Validate environment variables
    env_missing = [k for k, v in CONNECT_ARGS.items() if v in (None, "")]
    if env_missing:
        raise RuntimeError(f"Missing required env vars: {', '.join(env_missing)}")

    # Create database engine
    engine = create_engine(
        "oracle+oracledb://",
        connect_args=CONNECT_ARGS,
        future=True,
        pool_pre_ping=True,
        echo=False,
    )

    # Return configured sessionmaker
    return sessionmaker(bind=engine, future=True, expire_on_commit=False)
