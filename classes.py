import sqlite3, eel

class Company:
    def __init__(self) -> None:
        pass

class Portfolio:
    def __init__(self) -> None:
        pass

class Investor:
    def __init__(self) -> None:
        pass

class Order:
    def __init__(self) -> None:
        pass

class Transaction:
    def __init__(self) -> None:
        pass

class Quote:
    def __init__(self) -> None:
        pass

class PriceHistory:
    def __init__(self) -> None:
        pass

class User(Portfolio, Investor):
    def __init__(self) -> None:
        super().__init__()

    def get_user_login(self):
        pass

class Stock(Company, Order, Transaction, Quote, PriceHistory):
     def __init__(self,id:int, name:str, id_name:str, info:str, lot:int, price:float, publishing_stock:int) -> None:
        super().__init__()
        self.id_stock: int = id		    
        self.name: str = name               
        self.id_name: str = id_name             
        self.info: str = info                
        self.lot: int = lot                
        self.price: float = price               
        self.publishing_stock: int = publishing_stock    

class Exchange(User, Stock):
    def __init__(self) -> None:
        super().__init__()

class News:
    def __init__(self) -> None:
        self.news:list = []
    
    def get_news(self):
        pass

class Menu(News, Exchange):
    def __init__(self) -> None:
        super().__init__()
    


class Api(Menu):
    def __init__(self) -> None:
        super().__init__()
        self.initialize_eel()

    def initialize_eel(self):
        eel.init("birga_eel")
        eel.start("main.html", size=(1300, 600), mode="chrome")

    @eel.expose
    def vxod_api(login, password):
        pass

class SQLighter:
    def __init__(self, database: str = "db.db") -> None:
        self.connection = sqlite3.connect(database)
        self.cursor = self.connection.cursor()
        self.create_table()

    def create_table(self):
        with self.connection:
            pass

class Main:
    def __init__(self) -> None:
        self.DB = SQLighter()
        self.Api = Api()