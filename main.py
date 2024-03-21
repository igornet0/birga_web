from sqliter import SQLighter
from api import Api
from sys import argv
from hashlib import sha256

class Test:

    def __init__(self, db: SQLighter):
        self.db = db

    def test1(self):

        user = ["Igor Mickhaylets", "Igor_bot", sha256("12345678".encode('utf-8')).hexdigest()]

        if not self.db.user_on_login("Igor_bot"):
            self.db.add_user(*user)
        
        if sha256("12345678".encode('utf-8')).hexdigest() == self.db.user_on_login("Igor_bot")["password"]:
            return True
        return False

    def test2(self, login="Igor_bot"):
        return bool(self.db.user_on_login(login))
    
    def test3(self, login="Igor_bot", password="-0-0"):
        self.db.set_password(login, sha256(password.encode('utf-8')).hexdigest())
        return self.db.user_on_login("Igor_bot")["password"] != sha256("12345678".encode('utf-8')).hexdigest()
    
    def test5(self, login="Igor_bot"):
        user = self.db.user_on_login(login)
        return bool(user)




def main(debug=False):
    name_db = "db.db"
    db = SQLighter(name_db)
    if not db.get_news():
        from create_news import create_news
        create_news(name_db)
    
    if not db.get_list_stock():
        from create_stocks import create_stocks
        create_stocks(name_db)
    
    if debug:
        print("[TEST 1]",Test(db).test1())
        print("[TEST 2]",Test(db).test2())
        print("[TEST 3]",Test(db).test3())
        print("[TEST 4]",not Test(db).test3(password="12345678"))
        print("[TEST 5]",Test(db).test5())
        """
        Купить и продать акции
        Обменять валюту
        Сменить фото/пароль/имя пользователя/пополнить или снять деньги
        Посмотреть информацию про акцию 
        """

    api = Api(db)

if __name__ == "__main__":
    skript, *l = argv

    main(debug=bool(l))