import os


class Config:
    MONGO_URI = os.environ.get('MONGODB_URI', 'mongodb://localhost:27017/loginregister')
    # MONGO_URI = "mongodb://localhost:27017/loginregister"
    DEBUG = True

