import sqlite3 as sq


async def db_connect():
    global db, cur

    db = sq.connect('my_products.db')
    cur = db.cursor()

    cur.execute(
        "CREATE TABLE IF NOT EXISTS my_products(product_id INTEGER PRIMARY KEY, photo TEXT, title TEXT, description TEXT)")

    db.commit()


async def get_all_products_bd():
    products = cur.execute("SELECT * FROM my_products").fetchall()

    return products


async def create_new_product(state):
    async with state.proxy() as data:
        new_product = cur.execute("INSERT INTO my_products (photo, title, description) VALUES (?, ?, ?)",
                                  (data['photo'],
                                   data['title'],
                                   data['description']))
        db.commit()
    return new_product
