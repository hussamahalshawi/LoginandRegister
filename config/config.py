import os


class Config:
    MONGO_URI = os.environ.get('MONGODB_URI', 'mongodb://localhost:27017/loginregister')
    SECRET_KEY = os.environ.get('SECRET_KEY', 'your-secret-key')
    # MONGO_URI = "mongodb://localhost:27017/loginregister"
    DEBUG = True

