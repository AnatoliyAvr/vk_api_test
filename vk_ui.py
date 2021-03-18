import sqlite3
import time

from PyQt6 import QtWidgets

from vk_ui_client import Ui_MainWindow
import vk_api


class Vk_ui(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.db = sqlite3.connect('vk_group.db')
        self.cur = self.db.cursor()
        self.create_db()

        self.insert_message.pressed.connect(self.vk_insert_message)
        self.insert_id_group.pressed.connect(self.vk_insert_id_group)
        self.insert_photo.pressed.connect(self.vk_insert_photo)
        self.publish.pressed.connect(self.vk_publish)

    def create_db(self):
        self.cur.execute("""CREATE TABLE IF NOT EXISTS vk_message (
           ID INTEGER PRIMARY KEY,
           MESSAGE TEXT
       )""")

        self.cur.execute("""CREATE TABLE IF NOT EXISTS vk_id_group (
           ID INTEGER PRIMARY KEY,
           ID_GROUP TEXT
       )""")

        self.cur.execute("""CREATE TABLE IF NOT EXISTS vk_photo (
           ID INTEGER PRIMARY KEY,
           PHOTO TEXT
       )""")

        self.db.commit()

    def delete(self, db_name):
        self.cur.execute(f'DELETE FROM {db_name}')
        self.db.commit()

    def vk_insert_message(self):
        self.delete("vk_message")
        self.error_message.clear()
        if self.cur.fetchone() is None:
            self.cur.execute("INSERT INTO vk_message(MESSAGE) VALUES (?)", (self.message.toPlainText(),))
            self.db.commit()
        for value in self.cur.execute("SELECT * FROM vk_message"):
            self.error_message.append(value[1])

    def vk_insert_id_group(self):
        self.cur.execute(f"SELECT ID_GROUP FROM vk_id_group WHERE ID_GROUP = '{self.inter_id_group.text()}'")
        if self.cur.fetchone() is None:
            self.cur.execute("INSERT INTO vk_id_group(ID_GROUP) VALUES (?)", (self.inter_id_group.text(),))
            self.db.commit()
        for value in self.cur.execute("SELECT * FROM vk_id_group"):
            self.error_id_group.append(value[1])

    def vk_insert_photo(self):
        self.cur.execute(f"SELECT PHOTO FROM vk_photo WHERE PHOTO = '{self.inter_photo.text()}'")
        if self.cur.fetchone() is None:
            self.cur.execute("INSERT INTO vk_photo(PHOTO) VALUES (?)", (self.inter_photo.text(),))
            self.db.commit()
        for value in self.cur.execute("SELECT * FROM vk_photo"):
            self.error_photo.append(value[1])

    def vk_publish(self):
        vk_session = vk_api.VkApi(self.inter_login.text(),
                                  self.inter_password.text())
        try:
            vk_session.auth()
        except vk_api.AuthError as error_msg:
            print(error_msg)
            self.error_publish.append("Login is required to auth")
            return

        vk = vk_session.get_api()

        message = ""
        for count in self.cur.execute("SELECT * FROM vk_message"):
            message = count[1]

        id_group = []
        for count in self.cur.execute("SELECT * FROM vk_id_group"):
            id_group.append(count[1])

        str = ""
        for count in self.cur.execute("SELECT * FROM vk_photo"):
            str += f'{count[1]},'

        str1 = str[:-1]
        print(str1)

        for id_base in id_group:  # self.error_publish.append
            print(
                vk.wall.post(
                    message={message},
                    owner_id={id_base},
                    from_group=0,
                    attachments={str1}))
            time.sleep(2)


app = QtWidgets.QApplication([])
window = Vk_ui()
window.show()
app.exec()
