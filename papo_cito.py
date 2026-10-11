###################################################################################
###     ###     ###     ###     ###     ###     ###     ###     ###     ###     ###
###################################################################################
from flask import Flask, request, render_template, session, redirect, url_for   ###
from flask_sqlalchemy import SQLAlchemy                                         ###
from werkzeug.security import generate_password_hash, check_password_hash       ###
import json                                                                     ###
###################################################################################
app = Flask(__name__)                                                           ###    
                                                                                ###
###################################################################################
app.secret_key = "my-secret-key"                                                ###
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///users.db"                    ###
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False                            ###
###################################################################################
db = SQLAlchemy(app)                                                            ###    
                                                                                ###
###################################################################################
card_set_cards = db.Table(
    "card_set_cards",
    db.Column(
            "card_id",
            db.Integer,
            db.ForeignKey("cards.id"),
            primary_key=True
        ),
    db.Column(
            "set_id",
            db.Integer,
            db.ForeignKey("card_sets.id"),
            primary_key=True
    )
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

    user_id = db.Column(
            db.Integer,
            db.ForeignKey("pot_users.id"),
            nullable=False
        )
class CardSet(db.Model):
    __tablename__ = "card_sets"

    id = db.Column(db.Integer, primary_key=True)
    
    name = db.Column(db.String(100), nullable=False)

    user_id = db.Column(
            db.Integer,
            db.ForeignKey("pot_users.id"),
            nullable=False
        )

    cards = db.relationship(
            "Card",
            secondary=card_set_cards,
            backref=db.backref("sets", lazy="select")
        )

###################################################################################
with app.app_context():                                                         ###        
    db.create_all()                                                             ###    
###################################################################################
                                                                                ###
#def import_cards():                                                            ###
#    with open("data/cards.json", "r") as file:                                 ###
#        data_ingested = json.load(file)                                        ###
#    for items in data_ingested:                                                ###
#        new_card = Card(                                                       ###
#                question=items["question"],                                    ###
#                answer=items["answer"],                                        ###
#                user_id = int(session["user_id"])                              ###
#        )                                                                      ###
#        db.session.add(new_card)                                               ###
#    db.session.commit()                                                        ###
###################################################################################
@app.route("/bulk_action", methods=["GET", "POST"])
def bulk_action():
    if request.method == "POST":
        if "user_id" not in session:
            return redirect(url_for("login"))
        cards = Card.query.filter_by(
                user_id=session["user_id"]
                ).all()
        return redirect(url_for("cards", cards=cards))
    return render_template("cards.html")

@app.route("/cards", methods=["GET","POST"])                                    
def cards():                                                                    
    if request.method == "GET":                                                   
        user_id = session["user_id"]
        cards = Card.query.filter_by(
                user_id=user_id
                ).all()
        return render_template("cards.html", cards=cards)
@app.route("/delete_card", methods=["GET","POST"])
def delete_card():
    if request.method == "POST":
        return render_template("cards.html")
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
            return redirect(url_for("cards"))
    return render_template("create_card.html")


###################################################################################
@app.route("/view_users", methods=["GET","POST"])                               ###
def view_users():                                                               ###
    if request.method == "GET":                                                 ###
                                                                                ###      
        __monkeys = User.query.all()                                            ###
        return render_template("info.html", ab_users=__monkeys) ###   ###   ### ### 
###################################################################################
@app.route("/")                                                                 ###
def home():                                                                     ###  
    print("Wanna go HOME with me, dear?")                                       ###
    return render_template("home.html")                                         ###
###################################################################################
@app.route("/register", methods=["GET", "POST"])                                ###
def register():                                                                 ###
    if request.method == "POST":                                                ###
        ulman_name = request.form.get("username", "").strip()                   ###
        ulman_word = request.form.get("password", "")                           ###
                                                                                ###
        if not ulman_word or not ulman_name:                                    ###
            return render_template("register.html") 
                                                                                ###
        existing_user = User.query.filter_by(username=ulman_name).first()       ###
                                                                                ###
        if existing_user:                                                       ###
            return render_template("register.html")   
                                                                                ###
        ulman_word_hash = generate_password_hash(ulman_word)                    ###
                                                                                ###
        pappi = User(                                                           ###
                username = ulman_name,                                          ###
                password_hash = ulman_word_hash                                 ###
        )                                                                       ###
        db.session.add(pappi)                                                   ###
        db.session.commit()                                                     ###
        return redirect(url_for("login")) 
    return render_template("register.html")                 
###################################################################################
@app.route("/login", methods=["GET", "POST"])                                   ###
def login():                                                                    ###
    if request.method == "POST":                                                ###
        ulma_name = request.form.get("username", "").strip()                    ###
        ulma_word = request.form.get("password", "")                            ###
        pussy_user = User.query.filter_by( username = ulma_name ).first()       ###
        if pussy_user and check_password_hash(pussy_user.password_hash,         ###
                                              ulma_word):                       ###
            session.clear()                                                     ###
            session["user"] = pussy_user.username                               ###
            session["user_id"] = pussy_user.id                                  ###
            return redirect(url_for("home")) ###   ###   ###   ###   ###   ###  ###
        return render_template( ###   ###   ###   ###   ###   ###   ###   ###   ###
                "login.html",                                                   ### 
                error="Invalid username or password"                            ###
        )                                                                       ###
    print("GOT HERE") 
    return render_template("login.html") ###   ###   ###   ###   ###   ###   ## ###
###################################################################################
@app.route("/logout")                                                           ###
def logout():                                                                   ###
    session.pop("user", None)                                                   ###    
    session.pop("user_id", None)                                                ###
    session.clear()                                                             ###
    return redirect(url_for("home")) ###   ###   ###   ###   ###   ###   ###    ###
###################################################################################
@app.route("/profile", methods = ["GET", "POST"])                               ###
def profile():                                                                  ###
    if request.method == "GET":                                                 ###
        print("I hope Ellen's hairy pussy is soaking..wet #YUM")                ###
        return render_template("profile.html") ###   ###   ###   ###   ###   ## ###
###################################################################################
###      ###      ###      ###     ###     ###      ###     ###     ###     ### ###
      ###      ###      ###     ###     ###     ###     ###     ###     ###     ### 
   ###      ###     ###     ###     ###     ###     ###     ###     ###     ### ###
###     ###     ###     ###     ###     ###     ###     ###     ###     ###     ###
###################################################################################
if __name__ == '__main__':  ##   ###   ###   ###   ###   ###   ###   ###   ###  ###
    app.run(debug=True)   ###   ###   ###   ###   ###   ###   ###   ###   ###   ###
###################################################################################
###################################################################################

