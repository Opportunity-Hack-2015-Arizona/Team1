from pymongo import MongoClient
from werkzeug.security import generate_password_hash, check_password_hash


# Magic decorator for defining constants
def constant(f):
    def fset(self, value):
        raise TypeError

    def fget(self):
        return f()

    return property(fget, fset)


class Model:
    def __init__(self):
        pass

    @staticmethod
    @constant
    def COLLECTION_NAME():
        return Model.__name__

    def to_doc(self):
        return {}


class Post(Model):
    def __init__(self):
        Model.__init__(self)

    @staticmethod
    @constant
    def COLLECTION_NAME():
        return "posts"

    def to_doc(self):
        Model.to_doc(self)


class User(Model):

    def __init__(self, username, phone_number, password):
        Model.__init__(self)
        self.username = username
        self.phone_number = phone_number
        self.password_hash = generate_password_hash(password, "pbkdf2:sha256:10000")

    @staticmethod
    @constant
    def COLLECTION_NAME():
        return "users"

    def to_doc(self):
        return {"username": self.username, "phone_number": self.phone_number, "password_hash": self.password_hash}


class GideonDatabaseClient:
    @staticmethod
    @constant
    def DATABASE_NAME():
        return "test-database"

    def __init__(self):
        self.client = MongoClient("mongodb://localhost:27017/")
        self.db = self.client[GideonDatabaseClient.DATABASE_NAME()]

    def get_collection(self, model_cls):
        return self.db[model_cls.COLLECTION_NAME()]

    def insert(self, model_inst):
        model_cls = model_inst.__class__
        collection = self.db.get_collection(model_cls)
        return collection.insert_one(model_cls.to_doc()).inserted_id

    def find(self, inst_id, model_cls):
        collection = self.get_collection(model_cls)
        return collection.find_one({"_id": inst_id})