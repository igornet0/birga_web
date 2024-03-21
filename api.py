import eel
from sqliter import SQLighter
import hashlib

def balance_round(USER):
    valyte_d = {"₽":"rub", "€":"eur", "¥":"cny", "$":"usd"}
    for s,c in valyte_d.items():
        USER[f"balance_{c}"] = round(USER[f"balance_{c}"], 2)
    return USER

def sort_stocks(item):
    price_l = list(item[-1])
    valyte = price_l.pop()
    valyte_d = {"₽":1, "€":100, "¥":12, "$":90}
    price = float("".join(price_l)) * valyte_d[valyte]
    return price

class Api:
    DB = None
    USER = None

    def __init__(self, db: SQLighter):
        global DB 
        DB = db
        self.initialize_eel()

    def initialize_eel(self):
        eel.init("birga_eel")
        eel.start("main.html", size=(1300, 600), mode="chrome")

    @eel.expose
    def vxod_api(login, password):
        global USER
        user = DB.user_on_login(login)
        USER = user
        if user:
            password_write = hashlib.sha256(password.encode('utf-8')).hexdigest()
            if password_write == user["password"]:
                user.pop("password")
                return True, user
        return False, "Логин или пароль неверный"
    
    @eel.expose
    def set_password(password_new):
        global USER, DB
        DB.set_password(USER["login"], hashlib.sha256(password_new.encode('utf-8')).hexdigest())

    @eel.expose
    def check_password_old(password_old):
        global DB, USER
        password_write = hashlib.sha256(password_old.encode('utf-8')).hexdigest()
        return password_write == DB.user_on_login(USER["login"])["password"]

    @eel.expose
    def reg(login, password, username):
        user = DB.user_on_login(login)
        if not user:
            DB.add_user(username, login, hashlib.sha256(password.encode('utf-8')).hexdigest())
            return True, DB.user_on_login(login)
        return False, "Такой логин уже есть"

    @eel.expose
    def profile_process():
        global USER, DB
        if not USER is None:
            user = DB.user_on_login(USER["login"])
            user.pop("password")
            USER = balance_round(user)
            return user
        return []

    @eel.expose
    def add_balance(valyte, suma):
        global USER, DB
        USER[valyte] += float(suma)
        USER = balance_round(USER)
        DB.add_balance(USER["id_user"], valyte, USER[valyte])

    @eel.expose
    def user_profile_stock():
        global USER, DB
        if not USER is None:
            user = DB.user_on_login(USER["login"])
            USER = balance_round(user)
            return user
        return []

    @eel.expose
    def stock_profile_stock():
        global USER, DB
        if not USER is None:
            stocks: dict = DB.get_stocks_user(USER["id_user"])
            result = []
            for stock in stocks:
                info_stock = DB.get_info_stock(stock["id_stock"])[0]
                price_l = list(info_stock["price"])
                valyte = price_l.pop()
                price = float("".join(price_l))
                result.append([info_stock["id_stock"], info_stock["id_name"], info_stock["name"], info_stock["price"], stock["col_lot"], f"{round(stock['col_lot'] * price, 2)}{valyte}"])
            return result
        return []
    
    @eel.expose
    def get_info_stock(id_stock, flag=False):
        global DB
        info = DB.get_info_stock(id_stock)[0]
        if flag:
            price_l = list(info["price"])
            valyte = price_l.pop()
            price = float("".join(price_l))
            info["price"] = price
            return info, valyte
        return info
    
    @eel.expose
    def get_list_stock():
        global DB
        result = []
        for stock in DB.get_list_stock():
            result.append([stock["id_stock"], stock["id_name"], stock["name"], stock["price"]])
        return sorted(result, key=sort_stocks)
    
    @eel.expose
    def get_trans_stock(id_stock):
        global DB, USER
        trans:list = DB.get_trans_stock(USER["id_user"], id_stock)
        result = []
        for tran in trans:
            lot = DB.get_info_stock(tran["id_stock"])[0]["lot"]
            tran["type"] = "Покупка" if tran["type"] == 1 else "Продажа"
            price_l = list(str(tran["price"]))
            valyte = price_l.pop()
            price = float("".join(price_l))
            suma = f"{'+' if tran['type'] == 'Продажа' else '-'}{round(abs(tran['lot'])*price, 2)}{valyte}"
            tran = [tran["id_trans"], tran["type"], tran["datatime"], tran["lot"], tran["price"], suma]
            result.append(tran)
        return result

    @eel.expose
    def trans_stok(id_stock, lot, type):
        global DB, USER
        info = DB.get_info_stock(id_stock)[0]
        price_l = list(info["price"])

        valyte = price_l.pop()
        valyte_d = {"₽":"rub", "€":"eur", "¥":"cny", "$":"usd"}
        price = float("".join(price_l))
        col = int(info["lot"])
        lot = int(lot)
        balance_user = USER[f"balance_{valyte_d[valyte]}"]
        trans = col*lot*price

        user_stocks = DB.get_stock_user(USER["id_user"], id_stock)
        if user_stocks:
            if user_stocks[0]["col_lot"] - lot*col < 0 and type == 0:
                return False
        else:
            if type == 0:
                return False
            
        if (balance_user - trans < 0 and type == 1):
            return False
        else:
            if type == 0:
                lot = -lot
            from datetime import datetime
            USER[f"balance_{valyte_d[valyte]}"] -= col*lot*price
            DB.add_balance(USER["id_user"], f"balance_{valyte_d[valyte]}", USER[f"balance_{valyte_d[valyte]}"])
            DB.add_tranction(datetime.now().strftime("%d.%m.%Y %H:%M"), USER["id_user"], id_stock, type, info["price"], lot*col)
            user_stocks = DB.get_stock_user(USER["id_user"], id_stock)
            if user_stocks:
                DB.update_user_stork(USER["id_user"], id_stock, user_stocks[0]["col_lot"] + lot*col)
                if user_stocks[0]["col_lot"] + (lot*col) == 0:
                    DB.del_stock_user(USER["id_user"], id_stock)
                return True
            DB.add_user_storck(USER["id_user"], id_stock, col*lot)
            return True
    
    @eel.expose
    def suma_stock_lot(id_stock, lot):
        global DB
        info = DB.get_info_stock(id_stock)[0]
        price_l = list(info["price"])
        valyte = price_l.pop()
        price = float("".join(price_l))
        col = int(info["lot"])
        lot = int(lot)
        return f"{round(col*lot*price,2)}{valyte}", f"{lot} лот - {col*lot}шт"
    
    @eel.expose
    def get_news(n=4):
        global DB
        news = DB.get_news()

        from random import shuffle
        shuffle(news)
        return news[:n]
    
    @eel.expose
    def exit():
        global USER
        USER = None