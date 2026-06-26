from flask import Flask, render_template, request, redirect, url_for, flash, abort
import os

from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash


app = Flask(__name__, template_folder="templates")

app.config['SECRET_KEY'] = 'change-this-key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'

db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"


# 👤 MODEL
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)
class Patient(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    condition = db.Column(db.String(300))


# 🔌 USER LOADER
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


# 🏠 HOME
@app.route("/")
@login_required
def index():
    return render_template("index.html")


# 🧾 REGISTER
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            flash("این یوزر قبلاً ثبت شده")
            return redirect(url_for("register"))

        hashed_password = generate_password_hash(password, method='pbkdf2:sha256')

        new_user = User(username=username, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()

        return redirect(url_for("login"))

    return render_template("register.html")

# dashboard
@app.route("/dashboard")
@login_required
def dashboard():
    patients = Patient.query.all()
    return render_template("dashboard.html", patients=patients)
# add patient
@app.route("/add_patient", methods=["POST"])
@login_required
def add_patient():
    name = request.form["name"]
    age = request.form["age"]
    condition = request.form["condition"]

    new_patient = Patient(name=name, age=age, condition=condition)
    db.session.add(new_patient)
    db.session.commit()

    return redirect(url_for("dashboard"))

# 🔑 LOGIN
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        user = User.query.filter_by(username=username).first()

        if user and check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for("index"))
        else:
            flash("نام کاربری یا رمز اشتباهه")

    return render_template("login.html")


# 🚪 LOGOUT
@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("login"))


# 📄 DYNAMIC PAGE
@app.route("/<page>")
def show_page(page):
    page = page.lower()
    file_path = os.path.join(app.template_folder, f"{page}.html")

    if os.path.exists(file_path):
        return render_template(f"{page}.html")
    else:
        return "صفحه مورد نظر یافت نشد."


# 🧠 CREATE DB
with app.app_context():
    db.create_all()


# ▶️ RUN
if __name__ == "main":
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=True, host="0.0.0.0", port=port)