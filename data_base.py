import pymongo
from pymongo import MongoClient
from dotenv import load_dotenv
import cipher
import os

load_dotenv()

class DataBase:
    def __init__(self):
        data = MongoClient(os.getenv("DB_LOGIN"))
        self.collection = data["pronto"]["users"]

    def add_field(self, dialog_id, pronto_login, pronto_password):
        if self.if_id_exist(dialog_id):
            return

        pronto_password = cipher.cipher_in(pronto_login, pronto_password)
        pronto_login = cipher.cipher_in(pronto_password, pronto_login)

        clen = self.collection.count_documents({})
        if clen == 0:
            n = 0
        else:
            n = self.collection.find({})[clen - 1]["_id"] + 1
        
        self.collection.insert_one({"_id": n, \
                "telegram_id": dialog_id, \
                "login": pronto_login, \
                "password": pronto_password})

    def delete_field(self, dialog_id):
        self.collection.delete_one({"telegram_id": dialog_id})

    def get_login_password(self, dialog_id):
        point = self.collection.find_one({"telegram_id": dialog_id})
        login, password = point["login"], point["password"]

        login = cipher.cipher_out(password, login)
        password = cipher.cipher_out(login, password)

        return login, password

    def if_id_exist(self, dialog_id):
        if (self.collection.count_documents({"telegram_id": dialog_id})):
            return True
        else:
            return False