import sqlite3


db_name = "card.db"
conn = None
cursor = None


def open_db():
    global conn, cursor
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()


def close_db():
    cursor.close()
    conn.close()


def do(query):
    cursor.execute(query)
    conn.commit()


def clear_db():
    """Удаляет все таблицы"""
    open_db()
    query = """DROP TABLE IF EXISTS card"""
    do(query)
    close_db()


def create():
    """Создает таблицу"""

    open_db()
    cursor.execute("PRAGMA foreign_keys=on")
    query = """
    CREATE TABLE IF NOT EXISTS card
    (id INTEGER PRIMARY KEY,
    username VARCHAR,
    age INTEGER,
    password VARCHAR,
    text_1 VARCHAR,
    text_2 VARCHAR,
    text_3 VARCHAR,
    image_1 BLOB,
    image_2 BLOB,
    image_3 BLOB,
    link_1 VARCHAR,
    link_2 VARCHAR,
    link_3 VARCHAR,
    link_4 VARCHAR
    )
    """
    do(query)
    close_db()


def create_card(
    username,
    age,
    password,
    text_1,
    text_2,
    text_3,
    image_1,
    image_2,
    image_3,
    link_1,
    link_2,
    link_3,
    link_4,
):
    """
    Добавляет карточку в БД
    """

    query = """
    INSERT INTO card
    (username, age, password,
    text_1, text_2, text_3,
    image_1, image_2, image_3,
    link_1, link_2, link_3, link_4)
    VALUES
    (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """
    open_db()
    cursor.execute(
        query,
        (
            username,
            age,
            password,
            text_1,
            text_2,
            text_3,
            image_1,
            image_2,
            image_3,
            link_1,
            link_2,
            link_3,
            link_4,
        ),
    )
    conn.commit()
    close_db()


def get_card(username):
    """
    Возвращает карточку пользователя по username
    """

    query = """
    SELECT username, age,
    text_1, text_2, text_3,
    image_1, image_2, image_3,
    link_1, link_2, link_3, link_4
    FROM card
    WHERE username = ?
    """
    open_db()
    cursor.execute(query, (username,))
    result = cursor.fetchone()
    close_db()
    return result


def check_password(username, password):
    """
    Проверяет пароль пользователя
    """

    query = """
    SELECT password
    FROM card
    WHERE username = ?
    """
    open_db()
    cursor.execute(query, (username,))
    result = cursor.fetchone()
    close_db()
    if result is not None:
        if result[0] == password:
            return True
        else:
            return False
    else:
        return False


def user_exists(username):
    query = "SELECT 1 FROM card WHERE username = ?"
    open_db()
    cursor.execute(query, (username,))
    result = cursor.fetchone()
    close_db()
    return result is not None


def delete_card(username):
    """
    Удаляет карточку пользователя
    """

    query = "DELETE FROM card WHERE username = ?"
    open_db()
    cursor.execute(query, (username,))
    conn.commit()
    close_db()


def show(table):
    """
    Выводит содержимое таблицы
    """

    query = "SELECT * FROM " + table
    open_db()
    cursor.execute(query)
    print(cursor.fetchall())
    close_db()


def show_tables():
    show("card")


def main():
    clear_db()
    create()
    show_tables()


if __name__ == "__main__":
    main()
