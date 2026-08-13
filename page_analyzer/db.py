import os
import psycopg2
from psycopg2.extras import RealDictCursor
from dotenv import load_dotenv
import logging

load_dotenv()


def get_db_connection():
    database_url = os.getenv('DATABASE_URL')
    if not database_url:
        raise RuntimeError('DATABASE_URL is not set in the environment variables')
    try:
        conn = psycopg2.connect(database_url)
        return conn
    except psycopg2.OperationalError as e:
        logging.exception('Database connection error')
        raise RuntimeError(f'Failed to connect to the database: {e}')


def get_all_urls():
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            cur.execute('SELECT id, name, created_at FROM urls ORDER BY created_at DESC')
            result = cur.fetchall()
    return result


def get_url_by_id(id):
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            cur.execute('SELECT id, name, created_at FROM urls WHERE id = %s;', (id,))
            result = cur.fetchone()
    return result


def get_url_by_name(name):
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            cur.execute('SELECT id, name, created_at FROM urls WHERE name = %s;', (name,))
            result = cur.fetchone()
    return result


def insert_url(name):
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            cur.execute('SELECT id FROM urls WHERE name = %s;', (name,))
            existing = cur.fetchone()
            if existing:
                return existing[0]
            else:
                cur.execute('INSERT INTO urls (name) VALUES (%s) RETURNING id;', (name,))
                result = cur.fetchone()[0]
                conn.commit()
                return result
                