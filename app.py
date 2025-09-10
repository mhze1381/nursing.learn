import os
from flask import Flask, render_template, request, redirect, url_for, session
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3

app = Flask(__name__)
app.secret_key = "SECRET_KEY"  # تغییرش بده به یه چیز امن

# اتصال و ایجاد جدول کاربران اگر وجود نداشت
def init_db():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

init_db()

# صفحه اصلی یا ریدایرکت به login
@app.route('/login')
def home():
    return redirect(url_for('login'))

# ثبت نام
@app.route('/register', methods=['GET','POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = generate_password_hash(request.form['password'])

        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        try:
            cursor.execute("INSERT INTO users (username,email,password) VALUES (?,?,?)",
                           (username, email, password))
            conn.commit()
        except sqlite3.IntegrityError:
            conn.close()
            return "نام کاربری یا ایمیل قبلاً استفاده شده"
        conn.close()
        return redirect(url_for('login'))
    return render_template('register.html')

# ورود
@app.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE email=?", (email,))
        user = cursor.fetchone()
        conn.close()

        if user and check_password_hash(user[3], password):
            session['user_id'] = user[0]
            session['username'] = user[1]
            return redirect(url_for('dashboard'))
        else:
            return "ایمیل یا رمز اشتباه"
    return render_template('login.html')

# داشبورد
@app.route('/dashboard')
def dashboard():
    if 'user_id' in session:
        return render_template('dashboard.html', username=session['username'])
    else:
        return redirect(url_for('login'))

# خروج
@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))


@app.route("/")
def index():
    return render_template("index.html")

@app.route("/aski")
def aski():
    return render_template("aski.html")

@app.route("/emergency")
def Emergency():
    return render_template("Emergency.html")
@app.route("/nezam")
def nezam():
    return render_template("nezam.html")
@app.route("/learn")
def learn():
    return render_template("learn.html")
@app.route("/tarh")
def tarh():
    return render_template("tarh.html")
@app.route("/vam")
def vam():
    return render_template("vam.html")


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=True, host="0.0.0.0", port=port)

