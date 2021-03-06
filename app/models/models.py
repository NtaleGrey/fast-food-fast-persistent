import datetime

import psycopg2
from flask import jsonify
from psycopg2.extras import RealDictCursor

import app

from .database import Database

db = Database(app)


class Users:
    '''This class handles the storing of user credentials in the database'''

    def __init__(self,
                 username=None,
                 email=None,
                 password=None,
                 admin=None):
        self.username = username
        self.email = email
        self.password = password
        self.admin = admin

    def create_user(self):
        db.cur.execute("""INSERT INTO users( username, email, password, admin)
                             VALUES(%s,%s,%s,%s)""",
                       (
                           self.username,
                           self.email,
                           self.password,
                           self.admin
                       )
                       )
        db.conn.commit()


    def get_all_users(self):
        db.cur.execute("""SELECT id, username, email, admin FROM users""")
        db.conn.commit()
        all_users = db.cur.fetchall()
        return all_users


    def get_user(self, user):
        db.cur.execute("""SELECT * FROM users WHERE username = (%s)""", (user,))
        db.conn.commit()
        user = db.cur.fetchone()
        return user


    def get_user_by_id(self, user_id):
        db.cur.execute("""SELECT * FROM users WHERE id = (%s)""", (user_id,))
        db.conn.commit()
        user = db.cur.fetchone()
        return user


    def get_username(self, user_id):
        user_dict = self.get_user_by_id(user_id)
        return user_dict["username"]


    def get_admin_status(self):
        db.cur.execute(""" SELECT role FROM users""")
        db.conn.commit()
        admin_status = db.cur.fetchall()
        return admin_status


    def update_admin_status(self, user_id):
        db.cur.execute(
            """ UPDATE users SET  admin= True WHERE id = (%s) """, (user_id,))
        db.conn.commit()


class Menu:
    '''This class handles the storing of menu items into the database'''

    def __init__(self, menu_item=None, price=None):
        self.menu_item = menu_item
        self.price = price

    def add_item(self):
        db.cur.execute(
            """INSERT INTO menu(menu_item, price) VALUES (%s,%s)""",
            (
                self.menu_item,
                self.price
            )
        )
        db.conn.commit()


    def get_menu(self):
        db.cur.execute("""SELECT * FROM menu""")
        db.conn.commit()
        menu_list = db.cur.fetchall()
        return menu_list


    def update_menu(self, meal_id, menu_item, price):
        db.cur.execute(
            """ UPDATE menu SET menu_item = (%s) WHERE meal_id = (%s) """,
            (menu_item, meal_id))
        db.conn.commit()
        db.cur.execute(
            """ UPDATE menu SET price = (%s) WHERE meal_id = (%s) """, (price, meal_id))
        db.conn.commit()


    def get_meal_by_id(self, meal_id):
        db.cur.execute("""SELECT * FROM menu WHERE meal_id = (%s)""", (meal_id,))
        db.conn.commit()
        one_meal = db.cur.fetchone()
        return one_meal


    def get_menu_item(self, item):
        db.cur.execute("""SELECT * FROM menu WHERE menu_item = (%s)""", (item,))
        db.conn.commit()
        item = db.cur.fetchone()
        return item


    def get_meal(self, item):
        menu_item = self.get_menu_item(item)
        if menu_item is not None:   
            return menu_item["menu_item"]
        return


    def delete_meal(self, meal_id):
        db.cur.execute(
            "DELETE FROM menu WHERE meal_id = (%s)", (meal_id,))
        db.conn.commit()
        db.cur.execute("DELETE FROM menu WHERE meal_id = (%s)", (meal_id,))
        db.conn.commit()


    def get_meal_id(self, order):
        meal = self.get_menu_item(order)
        if meal is not None:
            return meal["meal_id"]
        return


class Orders:
    '''This class handles the storing of user orders into the database'''

    def __init__(self,
                user_id=None,
                menu_id=None,
                order_made=None,
                location=None,
                comment=None,
                made_by=None):
        self.user_id = user_id
        self.menu_id = menu_id
        self.order_made = order_made
        self.location = location
        self.comment = comment
        self.made_by = made_by

    def create_order(self):
        db.cur.execute(
            """INSERT INTO orders(user_id, menu_id, order_made, location, comment, made_by) VALUES (%s,%s,%s,%s,%s,%s)""",
            (
                self.user_id,
                self.menu_id,
                self.order_made,
                self.location,
                self.comment,
                self.made_by
            )
        )
        db.conn.commit()


    def get_orders(self):
        db.cur.execute(
            """SELECT id, made_by, order_made, location, comment, status, order_date FROM orders""")
        db.conn.commit()
        all_orders = db.cur.fetchall()
        return all_orders


    def get_order_by_id(self, order_id):
        db.cur.execute(
            """SELECT id, made_by, order_made, location, comment, status, order_date FROM orders WHERE id = (%s)""",
            (order_id,))
        db.conn.commit()
        one_order = db.cur.fetchone()
        return one_order


    def get_user_orders(self, made_by):
        db.cur.execute(
            """SELECT id, made_by, order_made, location, comment, status, order_date FROM orders WHERE made_by = (%s)""",
            (made_by,))
        db.conn.commit()
        user_orders = db.cur.fetchall()
        return user_orders


    def insert_response(self, status, order_id):
        if status == "Processing":
            db.cur.execute(
                """ UPDATE orders SET status = 'Processing' WHERE id = (%s) """, (order_id,))
            db.conn.commit()
        elif status == "Cancelled":
            db.cur.execute(
                """ UPDATE orders SET status = 'Cancelled' WHERE id = (%s) """, (order_id,))
            db.conn.commit()
        elif status == "Complete":
            db.cur.execute(
                """ UPDATE orders SET status = 'Complete' WHERE id = (%s) """, (order_id,))
            db.conn.commit()
        else:
            return jsonify({"message": "Add correct status"}), 405


"""..........................These tables will be used for tests.........................."""


def drop():
    db.query(""" DROP TABLE IF EXISTS users CASCADE """)
    db.query(""" DROP TABLE IF EXISTS menu CASCADE""")
    db.query(""" DROP TABLE IF EXISTS orders CASCADE""")
    db.conn.commit()


def initialize():
    db.query("""CREATE TABLE users(
            id serial PRIMARY KEY,
            username VARCHAR(255),
            email VARCHAR(255),
            password VARCHAR(255),
            admin BOOLEAN DEFAULT 'false'
            )
            """)

    db.query("""CREATE TABLE menu(
            meal_id serial PRIMARY KEY,
            menu_item VARCHAR(255),
            price INTEGER
        )
        """)

    db.query("""CREATE TABLE orders(
            id serial PRIMARY KEY,
            user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
            menu_id INTEGER REFERENCES menu(meal_id) ON DELETE CASCADE,
            order_made VARCHAR(255),
            location VARCHAR(255),
            comment VARCHAR(500),
            made_by VARCHAR(255),
            status VARCHAR(255) DEFAULT 'New',
            order_date TIMESTAMP DEFAULT NOW()
        )
            """)

    db.conn.commit()
