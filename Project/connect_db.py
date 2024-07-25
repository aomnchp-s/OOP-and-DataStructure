import sqlite3
from sqlite3 import Error

class ConnectDB:
    # def __init__(self) -> None:
    #     pass

    def create_connection(self):
        database = 'expense_tracker.sqlite3'
        try:
            self._cnx = sqlite3.connect(database)
        except Error as err:
            print(err)
        return self._cnx
    
    def create_table_category(self):
        sql = """
            CREATE TABLE IF NOT EXISTS category(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name text NOT NULL,
                type text NOT NULL,
                UNIQUE (name)
            );
        """
        try:
            c = self._cnx.cursor()
            c.execute(sql)
        except Error as err:
            print(err)

    def create_table_expense(self):
        sql = """
            CREATE TABLE IF NOT EXISTS expense(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                description text NOT NULL,
                amount float(9,2) NOT NULL,
                date text NOT NULL,
                expense_chanel text,
                bank text,
                category text NOT NULL,
                type text NOT NULL
            );
        """
        try:
            c = self._cnx.cursor()
            c.execute(sql)
        except Error as err:
            print(err)
    
    def insert_expense(self, cnx, description, amount, date, expense_chanel, bank, category, type):
        sql = """
            INSERT INTO expense(description, amount, date, expense_chanel, bank, category, type)
            VALUES(?, ?, ?, ?, ?, ?, ?)
        """
        params = (description, amount, date, expense_chanel, bank, category, type)
        try:
            c = cnx.cursor()
            c.execute(sql, params)
            cnx.commit()
        except Error as err:
            print(err)

    def insert_category(self, cnx, category, type):
        sql = """
            INSERT INTO category(name, type)
            VALUES(?, ?)
        """
        params = (category, type)
        try:
            c = cnx.cursor()
            c.execute(sql, params)
            cnx.commit()
        except Error as err:
            print(err)

    def select_category(self, cnx):
        sql = """
            SELECT* FROM category
        """
        try:
            c = cnx.cursor()
            c.execute(sql)
            category = c.fetchall()
            return category
        except Error as err:
            print(err)

    def delete_category(self, cnx, category_name):
        sql = """
            DELETE FROM category
            WHERE name = ?
        """
        params = (category_name,)
        try:
            c = cnx.cursor()
            c.execute(sql, params)
            cnx.commit()
        except Error as e:
            print(e)

    def update_category(self, cnx, category_name, category_edit):
        sql = """
            UPDATE category
            SET name = (?)
            WHERE name = (?)
        """
        params = (category_edit,category_name)
        try:
            c = cnx.cursor()
            c.execute(sql, params)
            cnx.commit()
        except Error as e:
            print(e)

    def inquiry_transaction(self, cnx, startDate, endDate):
        sql = """
            SELECT* FROM expense
            WHERE date BETWEEN (?) AND (?)
            ORDER BY date desc
        """
        params = (startDate,endDate)
        try:
            c = cnx.cursor()
            c.execute(sql, params)
            transections = c.fetchall()

            if not transections:
                return False
            else:
                return transections
        except Error as err:
            print(err)
    
    def group_transaction(self, cnx, startDate, endDate, types):
        sql = """
            SELECT count(id),category FROM expense
            WHERE date BETWEEN (?) AND (?)
            AND type = (?)
            GROUP BY category;     
        """
        params = (startDate, endDate, types)
        try:
            c = cnx.cursor()
            c.execute(sql, params)
            transections = c.fetchall()

            if not transections:
                return False
            else:
                return transections
        except Error as err:
            print(err)


