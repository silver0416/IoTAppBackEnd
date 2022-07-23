import random
import string
from IoTAppBackEnd import connectMySQL
import hashlib


sql = connectMySQL.connectMySQL()
do = "use IoTApp"
cursor = sql.cursor()
cursor.execute(do)


class account:
    def generate_encrypt_password(password):
        return hashlib.sha512(password.encode()).hexdigest()
    def generate_random_salt(length):
        return ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(length))

    def create(username, password,salt_length = 10):
        do = "SELECT `username` FROM `account`;"
        cursor.execute(do)
        result = cursor.fetchall()
        print(result)
        for i in result:
            if i[0] == username:
                return False
        SALT = account.generate_random_salt(salt_length)
        ENCRYPT_PASSWORD = account.generate_encrypt_password(password)+SALT
        
        try:
            do = f"INSERT INTO `account` (`user_id`, `username`, `password`) VALUES (NULL, '{username}', '{ENCRYPT_PASSWORD}');"
            cursor.execute(do)
            sql.commit()
            return True
        except Exception as e:
            print(e)
            return False
    def login(username, password):
        do = f"SELECT `password` FROM `account` WHERE `username` = '{username}';"
        cursor.execute(do)
        result = cursor.fetchall()
        if len(result) == 0:
            return False
        SALT = result[0][0][-10:]
        print(len(SALT))
        print(SALT)
        ENCRYPT_PASSWORD = account.generate_encrypt_password(password)+SALT
        print(ENCRYPT_PASSWORD)
        do = f"SELECT `username` FROM `account` WHERE `password` = '{ENCRYPT_PASSWORD}' and `username` = '{username}';"
        cursor.execute(do)
        result = cursor.fetchall()
        if len(result) == 0:
            return False
        return True
    def update_password(username, password):
        SALT = account.generate_random_salt(10)
        ENCRYPT_PASSWORD = account.generate_encrypt_password(password)+SALT
        do = f"UPDATE `account` SET `password` = '{ENCRYPT_PASSWORD}' WHERE `username` = '{username}';"
        cursor.execute(do)
        sql.commit()
        return True
    def get_user_id(username):
        do = f"SELECT `user_id` FROM `account` WHERE `username` = '{username}';"
        cursor.execute(do)
        result = cursor.fetchall()
        if len(result) == 0:
            return False
        return result[0][0]
    def get_username(user_id):
        do = f"SELECT `username` FROM `account` WHERE `user_id` = '{user_id}';"
        cursor.execute(do)
        result = cursor.fetchall()
        if len(result) == 0:
            return False
        return result[0][0]
    def change_password(username, old_password, new_password):
        if account.login(username, old_password):
            account.update_password(username, new_password)
            return True
        return False
    

# print(account.create("test", "test"))
# print(account.login("test", "test"))

class user_info:
    def create(user_id, name, phone, email):
        do = f"INSERT INTO `user_info` (`user_id`, `user_nickname`, `user_phone`, `user_email`) VALUES ('{user_id}', '{name}', '{phone}', '{email}');"
        cursor.execute(do)
        sql.commit()
    def get_user_info(user_id):
        do = f"SELECT * FROM `user_info` WHERE `user_id` = '{user_id}';"
        cursor.execute(do)
        result = cursor.fetchall()
        return result
    def update(user_id, name, phone, email):
        do = f"UPDATE `user_info` SET `user_nickname` = '{name}', `user_phone` = '{phone}', `user_email` = '{email}' WHERE `user_id` = '{user_id}';"
        cursor.execute(do)
        sql.commit()

class verify:
    def store_verification_code(type,verification_code ,address):
        do = f"INSERT INTO `alive_verification_code` (`verify_id`, `type`, `verification_code`,`start_time`, `address`) VALUES (NULL, '{type}', '{verification_code}',CURRENT_TIMESTAMP, '{address}');"
        cursor.execute(do)
        sql.commit()
    def get_verification_code(type, address):
        do = f"SELECT `verification_code` FROM `verify` WHERE `type` = '{type}' and `address` = '{address}';"
        cursor.execute(do)
        result = cursor.fetchall()
        if len(result) == 0:
            return False
        return result[0][0]
    def get_verify_time(code,address):
        do = f"SELECT `start_time` FROM `verify` WHERE `verification_code` = '{code}' and `address` = '{address}';"
        cursor.execute(do)
        result = cursor.fetchall()
        if len(result) == 0:
            return False
        return result[0][0]