from flask import Flask, request, render_template, session, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = "kill-fuck-marry"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///users.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)

with app.app_context():
    db.create_all()

@app.route("/view_users", methods=["GET","POST"])
def view_users():
    if request.method == "GET":
        cunt_monkeys = User.query.all()
        return render_template("info.html", users=cunt_monkeys)

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        existing_user = User.query.filter_by(username=username).first()

        if existing_user:
            return "Username already exists"

        password_hash = generate_password_hash(password)

        user = User(
                username=username,
                password_hash=password_hash
        )

        db.session.add(user)
        db.session.commit()

        return redirect(url_for("login"))

    return render_template("register.html")
@app.route("/dashboard")
def dashboard():
    if "user" not in session:
        return redirect(url_for("login"))
    return render_template("dashboard.html")
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        
        username = request.form["username"]
        password = request.form["password"]
       
        user = User.query.filter_by(username=username).first()
    
        if user and check_password_hash(user.password_hash, password):
            session.clear()
            session["user"] = user.username
            #session["logged-in"] = True
            #valid_login = User.    
            return redirect(url_for("dashboard"))
        
        #flash("Invalid username or password", "error")
        return render_template("login.html") 
    
    return render_template("login.html")

@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect(url_for("home"))
@app.route("/profile", methods = ["GET", "POST"])
def profile():
    if request.method == "GET":
        return render_template("profile.html")
    #if "username" not in session:
    #    return "You are not logged in"
    #return f"Welcome, {session['username']}!"

if __name__ == '__main__':
    app.run(debug=True)
