import bcrypt

class User:
    def __init__(self, custom_id, username, email, password):
        self.custom_id = custom_id
        self.username = username
        self.email = email
        self.password = password

    @staticmethod
    def to_dict(user):
        return {
            "_id": user.custom_id,
            "username": user.username,
            "email": user.email,
            "password": user.password
        }

    @staticmethod
    def get_user(email, mongo):
        user = mongo.db.users.find_one({"email": email})
        user = User(user['_id'], user['username'], user['email'], user['password'])
        return user

    @staticmethod
    def check_user(email, password, mongo):
        user = User.get_user(email, mongo)
        # if user.email == email and user.password == password:
        # print(user.password)
        if user:
            if bcrypt.checkpw(password, user.password):
                print('True')
                return user
            else:
                print('False')
        else:
            print('not found')

    # @staticmethod
    # def create_user(user):
    #     user = User.to_dict(user)
    #     return mongo.db.users.insert_one(user)

    @staticmethod
    def create_user(user, mongo):
        user_d = User.to_dict(user)
        return User.update_user(user.username, user_d, mongo)

    @staticmethod
    def update_user(username, user, mongo):
        return mongo.db.users.update_one({"username": username}, {"$set": user}, upsert=True)
