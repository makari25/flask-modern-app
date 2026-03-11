import sqlite3
from flask import Flask, render_template, request, url_for, flash, redirect

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key_here' # Required for session security

# Function to get a database connection
def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row # Allows accessing columns by name
    return conn

# Route: Home Page (Read Tasks)
@app.route('/')
def index():
    conn = get_db_connection()
    tasks = conn.execute('SELECT * FROM tasks').fetchall()
    conn.close()
    return render_template('index.html', tasks=tasks)

# Route: Create Task
@app.route('/create', methods=('GET', 'POST'))
def create():
    if request.method == 'POST':
        content = request.form['content']
        priority = request.form['priority']

        if not content:
            flash('Content is required!')
        else:
            conn = get_db_connection()
            conn.execute('INSERT INTO tasks (content, priority) VALUES (?, ?)',
                         (content, priority))
            conn.commit()
            conn.close()
            return redirect(url_for('index'))

    return render_template('create.html')

# Route: Delete Task
@app.route('/<int:id>/delete', methods=('POST',))
def delete(id):
    task = get_db_connection().execute('SELECT * FROM tasks WHERE id = ?', (id,)).fetchone()
    conn = get_db_connection()
    conn.execute('DELETE FROM tasks WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    flash('"{}" was successfully deleted!'.format(task['content']))
    return redirect(url_for('index'))

if __name__ == "__main__":
    app.run(debug=True)