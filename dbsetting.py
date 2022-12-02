import sqlite3

global db
db = sqlite3.connect('db.db')
sql = db.cursor()

# Сессии с источником и датой сессии
sql.execute("""CREATE TABLE IF NOT EXISTS ads (
    adid INT,
    title TEXT,
    title2 TEXT,
    text TEXT,
    
)""")

db.commit()

def DbAddAds(goods,price,adid,title,title2,description, available):
    sql.execute(f"SELECT goods FROM ads WHERE goods = '{goods}'")
    if sql.fetchone() is None:
        sql.execute(f"INSERT INTO ads ('goods', 'price', 'adid', 'title', 'title2', 'description', 'available') VALUES('{goods}', '{price}', '{adid}', '{title}', '{title2}', '{description}', '{available}')")
        db.commit()

def DbGetAds():
    sql.execute(f"SELECT * FROM ads")
    list = sql.fetchall()
    return list

def DbAdsUpdate(goods, price):
    sql.execute(f"UPDATE ads SET price = '{price}' WHERE goods = '{goods}'")
    db.commit()

def DbAdsUpdateAvailable(goods, available):
    sql.execute(f"UPDATE ads SET available = '{available}' WHERE goods = '{goods}'")
    db.commit()

def DbCleanDb():
    sql.execute(f"DELETE FROM ads")
    db.commit()