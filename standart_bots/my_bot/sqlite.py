import sqlite3
import sqlite3 as sq


async def db_connect() -> None:
    global db, cur

    db = sq.connect('my_products.db')
    cur = db.cursor()

    cur.execute(
        "CREATE TABLE IF NOT EXISTS my_products(product_id INTEGER PRIMARY KEY, photo TEXT, title TEXT, description TEXT)")

    db.commit()


async def get_all_products_bd() -> list:
    products = cur.execute("SELECT * FROM my_products").fetchall()
    return products


async def create_new_product(state) -> sqlite3.Cursor:
    async with state.proxy() as data:
        new_product = cur.execute("INSERT INTO my_products (photo, title, description) VALUES (?, ?, ?)",
                                  (data['photo'],
                                   data['title'],
                                   data['description']))
        db.commit()
        print(type(new_product))
    return new_product


async def delete_product(product_id: int) -> None:
    cur.execute("DELETE FROM my_products WHERE product_id = ?", (product_id,))
    db.commit()


async def edit_product(product_id: int, title: str) -> None:
    cur.execute("UPDATE my_products SET title = ? WHERE product_id = ?", (title, product_id,))
    db.commit()
