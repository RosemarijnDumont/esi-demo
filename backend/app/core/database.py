
import os
import psycopg2
from psycopg2.extensions import connection as pg_connection
from contextlib import contextmanager

from app.core.config import settings


@contextmanager
def get_db_connection() -> pg_connection:
    """
    Provides a context-managed connection to the primary database.
    """
    conn = None
    try:
        conn = psycopg2.connect(
            host=settings.DATABASE_HOST,
            database=settings.DATABASE_NAME,
            user=settings.DATABASE_USER,
            password=settings.DATABASE_PASSWORD,
            port=settings.DATABASE_PORT,
            options=f"-c statement_timeout={settings.DB_STATEMENT_TIMEOUT_MS}"
        )
        yield conn
    except psycopg2.Error as e:
        print(f"Database connection error: {e}")
        raise
    finally:
        if conn:
            conn.close()


@contextmanager
def get_read_replica_connection() -> pg_connection:
    """
    Provides a context-managed connection to the read-replica database.
    """
    conn = None
    try:
        conn = psycopg2.connect(
            host=settings.READ_REPLICA_HOST, # Configured to use a separate host
            database=settings.READ_REPLICA_NAME or settings.DATABASE_NAME,
            user=settings.READ_REPLICA_USER or settings.DATABASE_USER,
            password=settings.READ_REPLICA_PASSWORD or settings.DATABASE_PASSWORD,
            port=settings.READ_REPLICA_PORT or settings.DATABASE_PORT,
            options=f"-c statement_timeout={settings.DB_STATEMENT_TIMEOUT_MS}"
        )
        yield conn
    except psycopg2.Error as e:
        print(f"Read-replica connection error: {e}")
        # Fallback to primary if read-replica is unavailable or not configured correctly
        print("Falling back to primary database for read operation.")
        with get_db_connection() as primary_conn:
            yield primary_conn
    finally:
        if conn:
            conn.close()

