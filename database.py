import datetime
import psycopg2
from werkzeug.security import generate_password_hash, check_password_hash
from dotenv import load_dotenv
import os
load_dotenv()
DATABASE = os.getenv("DATABASE_URL")

def init_db() -> None:
    with psycopg2.connect(DATABASE) as conn:
        cursor = conn.cursor()

        cursor.execute('''
                CREATE TABLE IF NOT EXISTS users (
                    id SERIAL PRIMARY KEY, 
                    email TEXT,
                    password TEXT,
                    telegram_id BIGINT
            )
        ''')

        cursor.execute('''
                CREATE TABLE IF NOT EXISTS products (
                    id SERIAL PRIMARY KEY, 
                    url TEXT,
                    name TEXT,
                    threshold FLOAT,
                    active INTEGER,
                    user_id INTEGER
            )
        ''')

        cursor.execute('''
                CREATE TABLE IF NOT EXISTS history (
                    id SERIAL PRIMARY KEY, 
                    url TEXT,
                    name TEXT,
                    price FLOAT,
                    date TEXT,
                    user_id INTEGER
            )
        ''')

        conn.commit()

def add_user(email: str, password: str, telegram_id) -> None:
    hashed = generate_password_hash(password, method='scrypt', salt_length=16)
    try:
        with psycopg2.connect(DATABASE) as conn:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO users (email, password, telegram_id) VALUES (%s,%s,%s)",
                           (email, hashed, telegram_id))
            conn.commit()
    except Exception as E:
        print(f'Ha ocurrido un error al insertar un usuario: {E}')

def delete_user(user_id: int) -> None:
    try:
        with psycopg2.connect(DATABASE) as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM users WHERE id = %s", (user_id,))
            conn.commit()
    except Exception as e:
        print(f'Error al eliminar usuario: {e}')

def update_user(user_id, email, telegram_id):
    try:
        with psycopg2.connect(DATABASE) as conn:
            cursor = conn.cursor()
            cursor.execute("UPDATE users SET email = %s, telegram_id = %s WHERE id = %s", (email, telegram_id, user_id))
            conn.commit()
    except Exception as e:
        print(f'Error al actualizar el usuario: {e}')

def get_users():
    try:
        with psycopg2.connect(DATABASE) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM users")
            users = cursor.fetchall()
            return users
    except Exception as e:
        print(f'Error al obtener el email: {e}')
        return []

def get_user(user_id):
    try:
        with psycopg2.connect(DATABASE) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM users WHERE id = %s", (user_id,))
            user = cursor.fetchone()
            return user
    except Exception as e:
        print(f'Error al obtener el usuario: {e}')
        return []

def check_mail_exist(email_user: str) -> bool:
    try:
        with psycopg2.connect(DATABASE) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT email FROM users WHERE email = %s", (email_user,))
            email = cursor.fetchone()
            return email is not None
    except Exception as e:
        print(f'Error al obtener el email: {e}')
        return False

def get_id_from_email(email_user):
    try:
        with psycopg2.connect(DATABASE) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT id FROM users WHERE email = %s", (email_user,))
            user_id = cursor.fetchone()
            return user_id[0] if user_id else None
    except Exception as e:
        print(f'Error al obtener el email: {e}')
        return None

def check_password(email_user, password_user):
    try:
        with psycopg2.connect(DATABASE) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT password FROM users WHERE email = %s", (email_user,))
            password_hashed = cursor.fetchone()
            if password_hashed is None:
                return False
            return check_password_hash(password_hashed[0], password_user)
    except Exception as e:
        print(f'Error al obtener el email: {e}')
        return False


def add_product(url: str, name: str, threshold, user_id) -> None:
    try:
        with psycopg2.connect(DATABASE) as conn:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO products (url, name, threshold, active, user_id) VALUES (%s,%s,%s,1,%s)", (url, name, threshold,user_id))
            conn.commit()
    except Exception as E:
        print(f'Ha ocurrido un error al insertar un producto: {E}')

def delete_product(product_id: int) -> None:
    try:
        with psycopg2.connect(DATABASE) as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM products WHERE id = %s", (product_id,))
            conn.commit()
    except Exception as e:
        print(f'Error al eliminar producto: {e}')

def product_exists(url: str, user_id: int):
    try:
        with psycopg2.connect(DATABASE) as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT id FROM products WHERE url = %s AND user_id = %s",
                (url, user_id)
            )
            return cursor.fetchone() is not None
    except Exception as e:
        print(f'Error: {e}')

def get_active_products(user_id) -> list | None:
    try:
        with psycopg2.connect(DATABASE) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * from products WHERE active = 1 AND user_id = %s", (user_id,))
            active_products = cursor.fetchall()
            return active_products
    except Exception as E:
        print(f'Ha ocurrido un error al obtener los productos activos: {E}')
        return None

def save_price(url: str, name: str, price: float, user_id) -> None:
    try:
        with psycopg2.connect(DATABASE) as conn:
            cursor = conn.cursor()
            date = datetime.datetime.now()
            actual_time = date.strftime("%Y/%m/%d %H:%M:%S")
            cursor.execute("INSERT INTO history (url, name, price, date, user_id) VALUES (%s,%s,%s,%s,%s)", (url, name, price, actual_time, user_id))
            conn.commit()
    except Exception as E:
        print(f'Ha ocurrido un error al insertar un historial: {E}')

def delete_price(history_id: int) -> None:
    try:
        with psycopg2.connect(DATABASE) as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM history WHERE id = %s", (history_id,))
            conn.commit()
    except Exception as e:
        print(f'Error al eliminar registro: {e}')

def get_last_price(url: str, user_id) -> float | None:
    try:
        with psycopg2.connect(DATABASE) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT price from history WHERE url = %s AND user_id = %s ORDER BY id DESC LIMIT 1", (url,user_id))
            last_price = cursor.fetchone()
            return last_price[0] if last_price else None
    except Exception as E:
        print(f'Ha ocurrido un error al obtener el ultimo precio : {E}')
        return None

def get_history(url: str, user_id) -> list:
    try:
        with psycopg2.connect(DATABASE) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM history WHERE url = %s AND user_id = %s ORDER BY id DESC", (url,user_id))
            return cursor.fetchall()
    except Exception as e:
        print(f'Error al obtener historial: {e}')
        return []
