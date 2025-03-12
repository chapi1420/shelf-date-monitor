from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

DB_path = "C:\\Users\\beza\\Desktop\\CRUD\\example.db"

# Database setup
def init_db():
    conn = sqlite3.connect(DB_path)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS items (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            category TEXT NOT NULL,
            expiry_date TEXT NOT NULL,
            quantity INTEGER NOT NULL,
            unit TEXT NOT NULL,
            storage_location TEXT NOT NULL,
            notes TEXT
        )
    ''')
    conn.commit()
    conn.close()

# Get all items from the database
def get_items():
    conn = sqlite3.connect(DB_path)
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM items')
    items = cursor.fetchall()
    conn.close()
    return items

# Add an item to the database
def add_item(name, category, expiry_date, quantity, unit, storage_location, notes):
    conn = sqlite3.connect(DB_path)
    cursor = conn.cursor()
    cursor.execute('''INSERT INTO items (name, category, expiry_date, quantity, unit, storage_location, notes)
                      VALUES (?, ?, ?, ?, ?, ?, ?)''', (name, category, expiry_date, quantity, unit, storage_location, notes))
    conn.commit()
    conn.close()

# Update an item's details
def update_item(id, name, category, expiry_date, quantity, unit, storage_location, notes):
    conn = sqlite3.connect(DB_path)
    cursor = conn.cursor()
    cursor.execute('''UPDATE items SET name = ?, category = ?, expiry_date = ?, quantity = ?, unit = ?, storage_location = ?, notes = ?
                      WHERE id = ?''', (name, category, expiry_date, quantity, unit, storage_location, notes, id))
    conn.commit()
    conn.close()

# Delete an item by ID
def delete_item(id):
    conn = sqlite3.connect(DB_path)
    cursor = conn.cursor()
    cursor.execute('DELETE FROM items WHERE id = ?', (id,))
    conn.commit()
    conn.close()

# Home page to list items and show form to add a new item
@app.route('/')
def index():
    items = get_items()
    return render_template('index.html', items=items)

# Add item via POST request
@app.route('/add_item', methods=['POST'])
def add_item_route():
    name = request.form['name']
    category = request.form['category']
    expiry_date = request.form['expiry_date']
    quantity = request.form['quantity']
    unit = request.form['unit']
    storage_location = request.form['storage_location']
    notes = request.form['notes']
    add_item(name, category, expiry_date, quantity, unit, storage_location, notes)
    return redirect(url_for('index'))

# Update item via POST request
@app.route('/update_item/<int:id>', methods=['GET', 'POST'])
def update_item_route(id):
    if request.method == 'POST':
        name = request.form['name']
        category = request.form['category']
        expiry_date = request.form['expiry_date']
        quantity = request.form['quantity']
        unit = request.form['unit']
        storage_location = request.form['storage_location']
        notes = request.form['notes']
        update_item(id, name, category, expiry_date, quantity, unit, storage_location, notes)
        return redirect(url_for('index'))
    
    conn = sqlite3.connect(DB_path)
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM items WHERE id = ?', (id,))
    item = cursor.fetchone()
    conn.close()
    return render_template('update_item.html', item=item)

# Delete item via GET request
@app.route('/delete_item/<int:id>', methods=['GET'])
def delete_item_route(id):
    delete_item(id)
    return redirect(url_for('index'))

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
