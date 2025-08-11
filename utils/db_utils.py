import sqlite3
from contextlib import contextmanager

class DatabaseUtils:
    def __init__(self, db_path='ecommerce_test.db'):
        self.db_path = db_path

    # Context manager for database connection
    @contextmanager
    def get_connection(self):
        conn = sqlite3.connect(self.db_path)
        try:
            yield conn
        finally:
            conn.close()

    # Function to execute a query and return the results
    def execute_query(self, query, params=None):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            return cursor.fetchall()
    
    # Function to execute an update/insert/delete query 
    def execute_update(self, query, params=None):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            conn.commit()
            return cursor.rowcount
    
    # Function to get a user by username
    def get_user_by_username(self, username):
        query = 'SELECT * FROM users WHERE username = ?'
        result = self.execute_query(query, (username,))
        return result[0] if result else None

    # Function to check if a user exists
    def user_exists(self, username):
        return self.get_user_by_username(username) is not None

    # Function to get the count of users
    def get_user_count(self):
        result = self.execute_query('SELECT COUNT(*) FROM users')
        return result[0][0] if result else 0

    # Function to get the stock of a product
    def get_product_stock(self, product_id):
        query = 'SELECT stock FROM products WHERE id = ?'
        result = self.execute_query(query, (product_id,))
        return result[0][0] if result else None

    # Function to update the stock of a product
    def update_product_stock(self, product_id, new_stock):
        query = 'UPDATE products SET stock = ? WHERE id = ?'
        return self.execute_update(query, (new_stock, product_id))

    # Function to get order details
    def get_order_details(self, order_id):
        query = '''
            SELECT o.*, u.username
            FROM orders o
            JOIN users u ON o.user_id = u.id
            WHERE o.id = ?
        '''
        result = self.execute_query(query, (order_id,))
        return result[0] if result else None

    # Function to get the count of order items
    def get_order_items_count(self, order_id):
        query = 'SELECT COUNT(*) FROM order_items WHERE order_id = ?'
        result = self.execute_query(query, (order_id,))
        return result[0][0] if result else 0

    # Function to get orders by user
    def get_orders_by_user(self, user_id):
        query = 'SELECT * FROM orders WHERE user_id = ?'
        return self.execute_query(query, (user_id,))

    # Function to cleanup test data
    def cleanup_test_data(self):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('DELETE FROM order_items')
            cursor.execute('DELETE FROM orders')
            cursor.execute('DELETE FROM users WHERE username LIKE "test%"')
            conn.commit()

    def reset_product_stocks(self):
        default_stocks = {
            1: 10,
            2: 15,
            3: 20,
            4: 5,
            5: 8,
            6: 12
        }

        with self.get_connection() as conn:
            cursor = conn.cursor()
            for product_id, stock in default_stocks.items():
                cursor.execute('UPDATE products SET stock = ? WHERE id = ?', 
                (stock, product_id))
            conn.commit()