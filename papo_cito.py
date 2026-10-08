from flask import Flask, request, render_template, session, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
import json

app = Flask(__name__)

app.secret_key = "kill-fuck-marry"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///users.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
class Card(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    question = db.Column(db.String(200))
    answer = db.Column(db.Text)
with app.app_context():
    db.create_all()

def import_cards():
    with open("data/cards.json", "r") as file:
        data_ingested = json.load(file)
    for items in data_ingested:
        new_card = Card(
                question=items["question"],
                answer=items["answer"],
                user_id = session["user_id"]
        )
        
        db.session.add(new_card)
    
    db.session.commit()

@app.route("/cards", methods=["GET","POST"])
def cards():
    if request.method == "GET":
        import_cards()
        card_s = cards.query.all()
        
        return render_template("cards.html", cards=card_s)

@app.route("/view_users", methods=["GET","POST"])
def view_users():
    if request.method == "GET":
        cunt_monkeys = User.query.all()
        return render_template("info.html", users=cunt_monkeys)



@app.route("/")
def home():
    print("This goes where, Ellen?")
    print("You can put it anywhere")
    return render_template("home.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        ulman_name = request.form.get("username", "").strip()
        ulman_word = request.form.get("password", "")

        if not ulman_word or not ulman_name:
            return render_template("register.html")

        existing_user = User.query.filter_by(username=ulman_name).first()

        if existing_user:
            return render_template("register.html")

        ulman_word_hash = generate_password_hash(ulman_word)

        pappi = User(
                username = ulman_name,
                password_hash = ulman_word_hash
        )

        db.session.add(pappi)
        db.session.commit()

        return redirect(url_for("login"))

    return render_template("register.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        ulma_name = request.form.get("username", "").strip()
        ulma_word = request.form.get("password", "")
       
        pussy_user = User.query.filter_by( username = ulma_name ).first()
    
        if pussy_user and check_password_hash(pussy_user.password_hash, ulma_word):
            session.clear()
            session["user"] = pussy_user.username
            session["user_id"] = pussy_user.id
            return redirect(url_for("home"))
        
        return render_template(
                "login.html",
                error="Invalid username or password"
        ) 

    return render_template("login.html")

@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect(url_for("home"))

@app.route("/profile", methods = ["GET", "POST"])
def profile():
    if request.method == "GET":
        return render_template("profile.html")

if __name__ == '__main__':
    app.run(debug=True)
