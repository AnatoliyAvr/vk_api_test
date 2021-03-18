import sqlite3

import vk_api


def test(telephone, password):
    vk_session = vk_api.VkApi(telephone, password)

    try:
        vk_session.auth()
    except vk_api.AuthError as error_msg:
        print(error_msg)
        return

    vk = vk_session.get_api()
    print(vk.status.get(user_id='305901256'))
    print(vk.status.set(text='Hello'))

    # print(vk.wall.post(message='Hello world!', friends_only=1,
    # attachments="photo305901256_366560609%2Fphotos305901256, photo305901256_366369218%2Fphotos3059012566"))

    # print(vk_session.method("stats.get", {"user_id": "305901256"}))
    # print(vk_session.method("wall.post", {"owner_id": 305901256, "message": "QWER"}))


db = sqlite3.connect('vk_group.db')
cur = db.cursor()

message = 'Hello world!'
id_group = "-122103467"
id_group1 = "-199605670"
photo = "photo305901256_366560609%2Fphotos305901256"
photo1 = "photo305901256_457239030%2Fphotos305901256"


def create_db():
    cur.execute("""CREATE TABLE IF NOT EXISTS vk_message (
        ID INTEGER PRIMARY KEY,
        MESSAGE TEXT
    )""")

    cur.execute("""CREATE TABLE IF NOT EXISTS vk_id_group (
        ID INTEGER PRIMARY KEY,
        ID_GROUP TEXT
    )""")

    cur.execute("""CREATE TABLE IF NOT EXISTS vk_photo (
        ID INTEGER PRIMARY KEY,
        PHOTO TEXT
    )""")

    db.commit()


def delete(db_name):
    cur.execute(f'DELETE FROM {db_name}')
    db.commit()


def insert_message():
    delete("vk_message")
    if cur.fetchone() is None:
        cur.execute("INSERT INTO vk_message(MESSAGE) VALUES (?)", (message,))
        db.commit()
    for value in cur.execute("SELECT * FROM vk_message"):
        print(value)


def insert_id_group():
    cur.execute(f"SELECT ID_GROUP FROM vk_id_group WHERE ID_GROUP = '{id_group}'")
    if cur.fetchone() is None:
        cur.execute("INSERT INTO vk_id_group(ID_GROUP) VALUES (?)", (id_group,))
        db.commit()
    for value in cur.execute("SELECT * FROM vk_id_group"):
        print(value)


def insert_photo():
    cur.execute(f"SELECT PHOTO FROM vk_photo WHERE PHOTO = '{photo1}'")
    if cur.fetchone() is None:
        cur.execute("INSERT INTO vk_photo(PHOTO) VALUES (?)", (photo1,))
        db.commit()
    for value in cur.execute("SELECT * FROM vk_photo"):
        print(value)


def main(telephone, password):
    vk_session = vk_api.VkApi(telephone, password)

    try:
        vk_session.auth()
    except vk_api.AuthError as error_msg:
        print(error_msg)
        return
    vk_session.auth()

    vk = vk_session.get_api()
    print(vk)

    for id_base in id_group:
        print(vk.wall.post(message={message}, owner_id={id_base}, from_group=0, attachments={photo}))


if __name__ == "__main__":
    pass
    # create_db()
    # insert_id_group()
    # insert_photo()
    # main("+3751111111", "11111")
