##################################################################################

from flask import Flask, request, render_template, session, redirect, url_for   ##
from flask_sqlalchemy import SQLAlchemy 
from sqlalchemy import or_                                         ##
from werkzeug.security import generate_password_hash, check_password_hash       ##
import json                                                                     ##

##################################################################################

app = Flask(__name__)                                                           ##    
app.secret_key = "my-secret-key"                                                ##
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///users.db"                    ##
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False                            ##
db = SQLAlchemy(app)                                                            ##    

##################################################################################

card_set_cards = db.Table (
    "card_set_cards",
    db.Column("card_id", db.Integer, db.ForeignKey("cards.id"), primary_key=True),
    db.Column("set_id", db.Integer, db.ForeignKey("card_sets.id"), primary_key=True)
)

class User(db.Model):                                                           
    __tablename__ = "pot_users"                                                 
    id = db.Column(db.Integer, primary_key=True)                                
    username = db.Column(db.String(80), unique=True, nullable=False)            
    password_hash = db.Column(db.String(255), nullable=False)                   
    cards = db.relationship("Card", backref="owner")
    card_sets = db.relationship("CardSet", backref="owner")

class Card(db.Model):                                                           
    __tablename__ = "cards"
    id = db.Column(db.Integer, primary_key=True)                                
    question = db.Column(db.String(200))                                        
    answer = db.Column(db.Text)
    user_id = db.Column(db.Integer, db.ForeignKey("pot_users.id"), nullable=False)

class CardSet(db.Model):
    __tablename__ = "card_sets"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("pot_users.id"), nullable=False)
    cards = db.relationship("Card", secondary=card_set_cards, backref=db.backref("sets", lazy="select"))

###################################################################################

with app.app_context():                                                                 
    db.create_all()                                                                 

###################################################################################
@app.route("/sets/create", methods=["GET", "POST"])
def create_set():
    if "user_id" not in session:
        return redirect(url_for("login"))

    if request.method == "POST":
        name = request.form.get("name", "").strip()
        if name:
            new_set = CardSet(
                    name=name,
                    user_id=session["user_id"]
                    )
            db.session.add(new_set)
            db.session.commit()
            
            return redirect(url_for("my_sets"))

    return render_template("create_set.html")

@app.route("/sets")
def my_sets():
    if "user_id" not in session:
        return redirect(url_for("login"))

    sets = CardSet.query.filter_by(
            user_id=session["user_id"]
            ).order_by(CardSet.id.asc()).all()

    return render_template("sets.html", sets=sets)

@app.route("/sets/<int:set_id>")
def view_set(set_id):
    if "user_id" not in session:
        return redirect(url_for("login"))
    card_set = CardSet.query.filter_by(
            id=set_id,
            user_id=session["user_id"]
            ).first_or_404()

    return render_template("set_detail.html", card_set=card_set)
@app.route("/cards")                                    
def cards():
    if "user_id" not in session:
        return redirect(url_for("login"))

    return render_template("cards_dashboard.html")

@app.route("/cards/all")
def all_cards():
    if "user_id" not in session:
        return redirect(url_for("login"))

    user_cards = (Card.query.filter_by(user_id=session["user_id"]).order_by(Card.id.asc()).all())
    return render_template("cards.html", cards=user_cards)

@app.route("/create-card", methods=["GET", "POST"])
def create_card():
    if request.method == "POST":
        question = request.form.get("question", "").strip()
        answer = request.form.get("answer", "").strip()

        if question and answer:
            card = Card(
                    question=question,
                    answer=answer,
                    user_id=session["user_id"]
                    )
            db.session.add(card)
            db.session.commit()

        return redirect(url_for("all_cards"))
    
    return render_template("create_card.html")
@app.route("/delete_card/<int:card_id>", methods=["POST"])
def delete_card(card_id):
    if "user_id" not in session:
        return redirect(url_for("login"))
    card = Card.query.filter_by(
            id=card_id,
            user_id=session["user_id"]
            ).first_or_404()
    
    db.session.delete(card)
    db.session.commit()

    return redirect(url_for("all_cards"))

@app.route("/select_option", methods=["GET", "POST"])
def select_option():
    if request.method == "POST":
        return redirect(url_for("cards"))

@app.route("/") 
def home():  
    if "user_id" not in session:
        redirect(url_for("login"))
            
    return render_template("cards_dashboard.html")

@app.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":
    
        _name = request.form.get("username", "").strip()
        _word = request.form.get("password", "")               
        
        if not _word or not _name:
            return render_template("register.html") 
                                                                                
        existing_user = User.query.filter_by(username=_name).first()       
                                                                                
        if existing_user:                                                       
            return render_template("register.html")   

        _word_hash = generate_password_hash(_word)    
                                                                        
        pappi = User(username=_name, password_hash=_word_hash)

        db.session.add(pappi)                                                   
        db.session.commit()                                                     
        
        return redirect(url_for("login"))


    return render_template("register.html")                 

@app.route("/login", methods=["GET", "POST"])                                   
def login():                                                                    
    if request.method == "POST":       

        _name = request.form.get("username", "").strip()                    
        _word = request.form.get("password", "")                            
        
        _user = User.query.filter_by(username=_name).first()       
        
        if _user and check_password_hash(_user.password_hash, _word): 
            session.clear() 
            session["user"] = _user.username
            session["user_id"] = _user.id
            return redirect(url_for("home"))

        return render_template("login.html", error="Invalid username or password")                                                                       
    
    return render_template("login.html")

@app.route("/logout")
def logout():                                                                   
    session.pop("user", None)    
    session.pop("user_id", None)
    session.clear()
    return redirect(url_for("home"))

###################################################################################

if __name__ == '__main__':  
    app.run(debug=True)

###################################################################################

