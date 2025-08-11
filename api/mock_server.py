from flask import Flask, request, jsonify
import json
import sqlite3
from datetime import datetime
import uuid

app = Flask(__name__)

def init_db():
    conn = sqlite3.connect('ecommerce_test.db')
    cursor = conn.cursor()

    # Create the users table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            email TEXT UNIQUE NOT NULL,
            first_name TEXT NOT NULL,
            last_name TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    # Create the products table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            price REAL NOT NULL,
            stock INTEGER DEFAULT 0,
            description TEXT
        )
    ''')

    # Create the orders table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS orders (
            id TEXT PRIMARY KEY,
            user_id INTEGER,
            total_amount REAL,
            status TEXT DEFAULT 'pending',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    ''')

    # Create the order_items table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS order_items (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            order_id TEXT,
            product_id INTEGER,
            quantity INTEGER,
            price REAL,
            FOREIGN KEY (order_id) REFERENCES orders (id),
            FOREIGN KEY (product_id) REFERENCES products (id)
        )
    ''')

    # Insert sample products
    cursor.execute('''
        INSERT OR IGNORE INTO products (id, name, price, stock, description) VALUES
        (1, 'Sauce Labs Backpack', 29.99, 10, 'Backpack for the trendy person'),
        (2, 'Sauce Labs Bike Light', 9.99, 15, 'Light that shines bright'),
        (3, 'Sauce Labs Bolt T-Shirt', 15.99, 20, 'Get your testing superhero on'),
        (4, 'Sauce Labs Fleece Jacket', 49.99, 5, 'Keep warm and stylish'),
        (5, 'Sauce Labs Onesie', 7.99, 8, 'For the cutest test automation'),
        (6, 'Test.allTheThings() T-Shirt (Red)', 15.99, 12, 'This classic shirt')
    ''')

    conn.commit()
    conn.close()

# API Routes
@app.route('/api/users', methods=['GET'])
def get_users():
    conn = sqlite3.connect('ecommerce_test.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users')
    users = cursor.fetchall()
    conn.close()
    
    return jsonify({
        'users': [
            {
                'id': user[0],
                'username': user[1], 
                'email': user[2],
                'first_name': user[3],
                'last_name': user[4],
                'created_at': user[5]
            } for user in users
        ]
    })

@app.route('/api/users', methods=['POST'])
def create_user():
    data = request.get_json()
    
    required_fields = ['username', 'email', 'first_name', 'last_name']
    for field in required_fields:
        if field not in data:
            return jsonify({'error': f'{field} is required'}), 400
    
    try:
        conn = sqlite3.connect('ecommerce_test.db')
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO users (username, email, first_name, last_name)
            VALUES (?, ?, ?, ?)
        ''', (data['username'], data['email'], data['first_name'], data['last_name']))
        
        user_id = cursor.lastrowid
        conn.commit()
        conn.close()

        return jsonify({
            'id': user_id,
            'username': data['username'],
            'email': data['email'],
            'first_name': data['first_name'],
            'last_name': data['last_name'],
            'message': 'User created successfully'
        }), 201
    
    except sqlite3.IntegrityError as e:
        return jsonify({'error': f'User with email {data["email"]} already exists'}), 409

@app.route('/api/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    conn = sqlite3.connect('ecommerce_test.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users WHERE id = ?', (user_id,))
    user = cursor.fetchone()
    conn.close()

    if not user:
        return jsonify({'error': 'User not found'}), 404
    
    return jsonify({
        'id': user[0],
        'username': user[1], 
        'email': user[2],
        'first_name': user[3],
        'last_name': user[4],
        'created_at': user[5]
    })

@app.route('/api/products', methods=['GET'])
def get_products():
    conn = sqlite3.connect('ecommerce_test.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM products')
    products = cursor.fetchall()
    conn.close()

    return jsonify({
        'products': [
            {
                'id': product[0],
                'name': product[1],
                'price': product[2],
                'stock': product[3],
                'description': product[4]
            } for product in products
        ]
    })

@app.route('/api/products/<int:product_id>/stock', methods=['PUT'])
def update_product_stock(product_id):
    data = request.get_json()
    new_stock = data.get('stock')

    if new_stock is None:
        return jsonify({'error': 'Stock is required'}), 400
    
    conn = sqlite3.connect('ecommerce_test.db')
    cursor = conn.cursor()
    cursor.execute('UPDATE products SET stock = ? WHERE id = ?', (new_stock, product_id))

    if cursor.rowcount == 0:
        conn.close()
        return jsonify({'error': 'Product not found'}), 404
    
    conn.commit()
    conn.close()

    return jsonify({'message': 'Product stock updated successfully', 'new_stock': new_stock})

@app.route('/api/orders', methods=['POST'])
def create_order():
    data = request.get_json()
    
    required_fields = ['user_id', 'items']
    for field in required_fields:
        if field not in data:
            return jsonify({'error': f'{field} is required'}), 400
    
    order_id = str(uuid.uuid4())
    total_amount = 0
    
    conn = sqlite3.connect('ecommerce_test.db')
    cursor = conn.cursor()
    
    try:
        # Calculate total and validate products
        for item in data['items']:
            product_id = item['product_id']
            quantity = item['quantity']
            
            cursor.execute('SELECT price, stock FROM products WHERE id = ?', (product_id,))
            product = cursor.fetchone()
            
            if not product:
                return jsonify({'error': f'Product {product_id} not found'}), 404
            
            price, stock = product
            if stock < quantity:
                return jsonify({'error': f'Not enough stock for product {product_id}'}), 400
            
            total_amount += price * quantity

        # Insert order into the database
        cursor.execute('''
            INSERT INTO orders (id, user_id, total_amount, status)
            VALUES (?, ?, ?, 'completed')
        ''', (order_id, data['user_id'], total_amount))
        
        # Create order items and update stock
        for item in data['items']:
            product_id = item['product_id']
            quantity = item['quantity']
            
            cursor.execute('SELECT price FROM products WHERE id = ?', (product_id,))
            price = cursor.fetchone()[0]
            
            cursor.execute('''
                INSERT INTO order_items (order_id, product_id, quantity, price)
                VALUES (?, ?, ?, ?)
            ''', (order_id, product_id, quantity, price))
            
            # Update stock
            cursor.execute('''
                UPDATE products SET stock = stock - ? WHERE id = ?
            ''', (quantity, product_id))
        
        conn.commit()
        conn.close()

        return jsonify({
            'order_id': order_id,
            'total_amount': total_amount,
            'status': 'completed',
            'message': 'Order created successfully'
        }), 201
    
    except Exception as e:
        conn.rollback()
        conn.close()
        return jsonify({'error': str(e)}), 500
    
@app.route('/api/orders/<order_id>', methods=['GET'])
def get_order(order_id):
    conn = sqlite3.connect('ecommerce_test.db')
    cursor = conn.cursor()

    cursor.execute('''
        SELECT o.*, u.username
        FROM orders o
        JOIN users u ON o.user_id = u.id
        WHERE o.id = ?
    ''', (order_id,))

    order = cursor.fetchone()

    if not order:
        conn.close()
        return jsonify({'error': 'Order not found'}), 404
    
    # Get order items
    cursor.execute('''
        SELECT oi.*, p.name 
        FROM order_items oi 
        JOIN products p ON oi.product_id = p.id 
        WHERE oi.order_id = ?
    ''', (order_id,))
    
    items = cursor.fetchall()
    conn.close()
    
    return jsonify({
        'order_id': order[0],
        'user_id': order[1],
        'username': order[5],
        'total_amount': order[2],
        'status': order[3],
        'created_at': order[4],
        'items': [
            {
                'product_id': item[2],
                'product_name': item[5],
                'quantity': item[3],
                'price': item[4]
            } for item in items
        ]
    })

if __name__ == '__main__':
    init_db()
    app.run(debug=True, port=5000)