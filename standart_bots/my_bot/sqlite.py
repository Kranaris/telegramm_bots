import sqlite3 as sq


async def db_connect():
    global db, cur

    db = sq.connect('my_products.db')
    cur = db.cursor()

    cur.execute(
        "CREATE TABLE IF NOT EXISTS my_products(product_id INTEGER PRIMARY KEY, name TEXT, price, description TEXT)")

    db.commit()

async def get_all_products_bd():

    products = cur.execute("SELECT * FROM my_products").fetchall()

    return products
async def add_profile(state, user_id):
    async with state.proxy() as data:
        cur.execute(
            "UPDATE profiles SET photo = '{}', age = '{}', description = '{}', name = '{}' WHERE user_id == '{}'".format(
                data['photo'], data['age'], data['description'], data['name'], user_id))
        db.commit()
