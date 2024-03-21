import sqlite3

def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d

class SQLighter:

    def __init__(self, database):
        self.connection = sqlite3.connect(database)
        self.cursor = self.connection.cursor()
        self.create_table()

    def create_table(self):
        with self.connection:

            self.cursor.execute('''CREATE TABLE IF NOT EXISTS Stock (
        						id_stock         INTEGER      NOT NULL PRIMARY KEY
                                                                   REFERENCES User_Stock (id_stock) 
                                                                   REFERENCES Tranction (id_stock),
                                name             STRING(20)   NOT NULL,
                                id_name          STRING(10)   NOT NULL,
                                info             STRING(500)  NOT NULL,
                                lot              INTEHER(20)  NOT NULL,
                                price            STRING(10)   NOT NULL,
                                publishing_stock INTEHER(20)  NOT NULL
        						)''')

            self.cursor.execute('''CREATE TABLE IF NOT EXISTS User (
        						id_user         INTEGER    NOT NULL PRIMARY KEY
                                                                REFERENCES User_Stock (id_user) 
                                                                REFERENCES Tranction (id_user),
                                name            STRING(20) NOT NULL,
                                login           STRING(20) NOT NULL,
                                password        STRING(20) NOT NULL,
                                balance_rub     REAL       DEFAULT(0),
                                balance_usd     REAL       DEFAULT(0),
                                balance_eur     REAL       DEFAULT(0),
                                balance_cny     REAL       DEFAULT(0)
        						)''')
            
            self.cursor.execute('''CREATE TABLE IF NOT EXISTS User_Stock (
                                id           INTEGER NOT NULL PRIMARY KEY,
                                id_user      INTEGER NOT NULL,
                                id_stock     INTEGER NOT NULL,
                                col_lot      INTEGER NOT NULL CHECK (col_lot > 0)
        						)''')
            
            self.cursor.execute('''CREATE TABLE IF NOT EXISTS Tranction (
        						id_trans    INTEGER      NOT NULL PRIMARY KEY,
                                datatime    STRING(20)   NOT NULL,
                                id_user     INTEGER      NOT NULL REFERENCES User (id_user),
                                id_stock    INTEGER      NOT NULL REFERENCES Stock (id_stock),
                                type        INTEGER(1)   NOT NULL,
                                price       STRING(20)   NOT NULL,
                                lot         INTEHER(20)  NOT NULL DEFAULT (0) 
        						)''')
            
            self.cursor.execute('''CREATE TABLE IF NOT EXISTS News (
        						id_new     INTEGER NOT NULL PRIMARY KEY,
                                text_new   STRING(500),
                                datetime   STRING(20)
        						)''')
            


    def add_user(self, name, login, password):
        with self.connection:
            self.cursor.execute("INSERT INTO `User` (`name`, `login`, `password`, `balance_rub`, `balance_usd`, `balance_eur`, `balance_cny`) VALUES(?,?,?,?,?,?,?)",
                                (name, login, password, 0, 0, 0, 0))

    def add_stock(self, name, name_id, info, lot, price, publishing_stock):
        with self.connection:
            self.cursor.execute("INSERT INTO `Stock` (`name`, `id_name`, `info`, `lot`, `price`, `publishing_stock`) VALUES(?,?,?,?,?,?)",
                                (name, name_id, info, lot, price, publishing_stock,))
            
    def add_new(self, text_new, datetime):
        with self.connection:
            self.cursor.execute("INSERT INTO `News` (`text_new`, `datetime`) VALUES(?,?)",
                                (text_new, datetime,))
            
    def get_news(self):
        with self.connection:
            news = self.cursor.execute("SELECT * FROM `News`").fetchall()
            return news
            
    def add_tranction(self, datatime, id_user, id_stock, type, price, lot):
        with self.connection:
            self.cursor.execute("INSERT INTO `Tranction` (`datatime`, `id_user`, `id_stock`, `type`, `price`, `lot`) VALUES(?,?,?,?,?,?)",
                                (datatime, id_user, id_stock, type, price, lot,))
            
    def add_user_storck(self, id_user, id_stock, col_lot):
        with self.connection:
            self.cursor.execute("INSERT INTO `User_Stock` (`id_user`, `id_stock`, `col_lot`) VALUES(?,?,?)",
                                (id_user, id_stock, col_lot,))
            
    def update_user_stork(self, id_user, id_stock, col_lot):
         with self.connection:
            self.cursor.execute(f"UPDATE `User_Stock` SET `col_lot` = ? WHERE `id_user` = ? AND `id_stock` = ?", (col_lot, id_user, id_stock,))

    def user_on_login(self, login:str) -> dict:
        with self.connection:
            user = self.cursor.execute("SELECT * FROM `User` WHERE `login` = ?", (login,))
            user.row_factory = dict_factory
            user = user.fetchall()
        return user[0] if user else user 
    
    def add_balance(self, id, valyte, suma):
        with self.connection:
            self.cursor.execute(f"UPDATE `User` SET `{valyte}` = ? WHERE `id_user` = ?", (suma, id,))

    def get_stocks_user(self, id_user):
        with self.connection:
            stock = self.cursor.execute("SELECT * FROM `User_Stock` WHERE `id_user` = ?", (id_user,)).fetchall()
        return stock if stock else []
    
    def get_stock_user(self, id_user, id_stock):
        with self.connection:
            stock = self.cursor.execute("SELECT * FROM `User_Stock` WHERE `id_user` = ? AND `id_stock` = ?", (id_user, id_stock,)).fetchall()
        return stock if stock else []
    
    def set_password(self, login, password_new):
        with self.connection:
            self.cursor.execute(f"UPDATE `User` SET `password` = ? WHERE `login` = ?", (password_new, login,))

    def get_info_stock(self, id_stock):
        with self.connection:
            stock = self.cursor.execute("SELECT * FROM `Stock` WHERE `id_stock` = ?", (id_stock,)).fetchall()
        return stock
    
    def get_trans_stock(self, id_user, id_stock):
        with self.connection:
            trans = self.cursor.execute("SELECT * FROM `Tranction` WHERE `id_stock` = ? AND `id_user` = ?", (id_stock, id_user,)).fetchall()
        return trans if trans else []
    
    def get_list_stock(self):
        with self.connection:
            stocks = self.cursor.execute("SELECT * FROM `Stock`").fetchall()
        return stocks

    def del_stock_user(self, id_user, id_stock):
        with self.connection:
            self.cursor.execute(f"DELETE FROM `User_Stock` WHERE `id_user` = ? AND `id_stock` = ?", (id_user, id_stock,))