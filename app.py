import sqlite3
from flask import Flask, render_template, request, redirect, url_for
from datetime import datetime

app = Flask(__name__)

def get_db_connection():
    conn = sqlite3.connect('business_data.db')
    conn.row_factory = sqlite3.Row
    return conn

# Database Tables Initialization
def init_db():
    conn = get_db_connection()
    # 1. Business Profile
    conn.execute('CREATE TABLE IF NOT EXISTS business (id INTEGER PRIMARY KEY, name TEXT)')
    # 2. Items & Stock (Cost is Optional)
    conn.execute('''CREATE TABLE IF NOT EXISTS items 
                    (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                     name TEXT UNIQUE, 
                     cost REAL DEFAULT 0, 
                     price REAL, 
                     stock INTEGER DEFAULT 0)''')
    # 3. Sales/Transactions
    conn.execute('''CREATE TABLE IF NOT EXISTS sales 
                    (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                     item_id INTEGER, 
                     qty INTEGER, 
                     total REAL, 
                     date TEXT,
                     FOREIGN KEY(item_id) REFERENCES items(id))''')
    conn.commit()
    conn.close()

init_db()

@app.route('/')
def index():
    conn = get_db_connection()
    biz = conn.execute('SELECT * FROM business LIMIT 1').fetchone()
    conn.close()
    return redirect(url_for('dashboard')) if biz else render_template('setup.html')

# Item Modify & Add (Cost Optional)
@app.route('/save-item', methods=['POST'])
def save_item():
    name = request.form['name']
    cost = request.form.get('cost') or 0 # Optional logic
    price = request.form['price']
    stock = request.form.get('stock') or 0
    
    conn = get_db_connection()
    conn.execute('INSERT OR REPLACE INTO items (name, cost, price, stock) VALUES (?, ?, ?, ?)',
                 (name, cost, price, stock))
    conn.commit()
    conn.close()
    return redirect(url_for('dashboard'))

# Billing & Auto Stock Update
@app.route('/create-bill', methods=['POST'])
def create_bill():
    item_id = request.form['item_id']
    qty = int(request.form['qty'])
    total = float(request.form['total'])
    date = datetime.now().strftime("%Y-%m-%d")

    conn = get_db_connection()
    # 1. Sale Record Karo
    conn.execute('INSERT INTO sales (item_id, qty, total, date) VALUES (?, ?, ?, ?)',
                 (item_id, qty, total, date))
    # 2. Stock Minus Karo
    conn.execute('UPDATE items SET stock = stock - ? WHERE id = ?', (qty, item_id))
    conn.commit()
    conn.close()
    return redirect(url_for('daybook'))

# Stock Summary Route
@app.route('/stock')
def stock_summary():
    conn = get_db_connection()
    inventory = conn.execute('SELECT name, stock, cost, price FROM items').fetchall()
    conn.close()
    return render_template('stock.html', inventory=inventory)

if __name__ == '__main__':
    app.run(debug=True)
