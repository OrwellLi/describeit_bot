import sqlite3

class Database:
    def __init__(self, db_file):
        self.connection = sqlite3.connect(db_file)
        self.cursor = self.connection.cursor()

 
    def add_user(self, user_id):
        with self.connection:
            a = self.cursor.execute("INSERT INTO `users` (`user_id`) VALUES (?)", (user_id,))
            return a
        
    def add_users_balance(self, user_id):
        with self.connection:
            b = self.cursor.execute("INSERT INTO `users_balance` (`user_id`) VALUES (?)", (user_id,))
            return b
    
    def add_users_product(self, user_id):
        with self.connection:
            b = self.cursor.execute("INSERT INTO `user_product` (`user_id`) VALUES (?)", (user_id,))
            return b

    def user_exists(self, user_id):
        with self.connection:
            result = self.cursor.execute("SELECT * FROM `users` WHERE `user_id` = ?", (user_id,)).fetchall()
            return bool(len(result))
    
    def set_nickname(self, user_id, nickname):
        with self.connection:
            return self.cursor.execute("UPDATE `users` SET `nickname` = ? WHERE `user_id` = ?", (nickname, user_id,))
    
    def get_signup(self, user_id):
        with self.connection:
            result = self.cursor.execute("SELECT `status` FROM `users` WHERE `user_id` = ?", (user_id,)).fetchall()
            for row in result:
                signup = str(row[0])
            return signup
    

    def set_signup(self, user_id, signup):
        with self.connection:
            return self.cursor.execute("UPDATE `users` SET `status` = ? WHERE `user_id` = ?", (signup, user_id,))
        
    
    def get_nickname(self, user_id):
        with self.connection:
            result = self.cursor.execute("SELECT `nickname` FROM `users` WHERE `user_id` = ?", (user_id,)).fetchall()
            for row in result:
                nickname = str(row[0])
            return nickname
    
    def check_balance(self, user_id):
        with self.connection:
            balance = self.cursor.execute("SELECT `user_balance` FROM `users_balance` WHERE `user_id` = ?", (user_id,)).fetchall()
            return balance
        
    def minus_balance(self, user_id, balance):
        with self.connection:
            return self.cursor.execute("UPDATE `users_balance` SET `user_balance` = user_balance - (?) WHERE `user_id` = ?", (1, user_id,))
    
    def plus_balance(self, user_id, balance):
        with self.connection:
            return self.cursor.execute("UPDATE `users_balance` SET `user_balance` = user_balance + (?) WHERE `user_id` = ?", (5, user_id,))
        
    def get_key(self, user_id):
        with self.connection:
            result = self.cursor.execute("SELECT `key` FROM `user_product` WHERE `user_id` = ?", (user_id,)).fetchall()
            for row in result:
                signup = str(row[0])
            return signup
    
    def set_key(self, user_id, last_key_phrase):
        with self.connection:
            return self.cursor.execute("UPDATE `user_product` SET `key` = ? WHERE `user_id` = ?", (last_key_phrase, user_id,))
    
    # def get_product_name(self, user_id):
    #     with self.connection:
    #         result = self.cursor.execute("SELECT `product_name` FROM `user_product` WHERE `user_id` = ?", (user_id,)).fetchall()
    #         for row in result:
    #             signup = str(row[0])
    #         return signup

    def set_product_name(self, user_id, prod_name):
        with self.connection:
            return self.cursor.execute("UPDATE `user_product` SET `product_name` = ? WHERE `user_id` = ?", (prod_name, user_id,))
        

    # def get_product_descrip(self, user_id):
    #     with self.connection:
    #         result = self.cursor.execute("SELECT `product_descrip` FROM `user_product` WHERE `user_id` = ?", (user_id,)).fetchall()
    #         for row in result:
    #             signup = str(row[0])
    #         return signup
        
    def set_product_descrip(self, user_id, prod_descrip):
        with self.connection:
            return self.cursor.execute("UPDATE `user_product` SET `product_descrip` = ? WHERE `user_id` = ?", (prod_descrip, user_id,))

    def get_product_key(self, user_id):
            with self.connection:
                result = self.cursor.execute("SELECT `product_keys` FROM `user_product` WHERE `user_id` = ?", (user_id,)).fetchall()
                for row in result:
                    signup = str(row[0])
                return signup

    def set_product_key(self, user_id, last_key_phrase):
        with self.connection:
            return self.cursor.execute("UPDATE `user_product` SET `product_keys` = ? WHERE `user_id` = ?", (last_key_phrase, user_id,))

    
    def get_promo(self, promo_id):
        with self.connection:
            result = self.cursor.execute("SELECT `promo_code` FROM `promocodes` WHERE `promo_id` = ?", (promo_id,)).fetchall()
            for row in result:
                signup = str(row[0])
            return signup
    