##################################################################################
from flask import Flask, request, render_template, session, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import or_
from werkzeug.security import generate_password_hash, check_password_hash
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

@app.route("/cards/search")
def search_cards():
    if "user_id" not in session:
        return redirect(url_for('login'))
    query = request.args.get("q", "").strip()
    results = []
    if query:
        pattern = f"%{query}%"
        results = Card.query.filter(
            Card.user_id == session["user_id"],
            or_(
                Card.question.ilike(pattern),
                Card.answer.ilike(pattern)
            )
        ).order_by(Card.id.asc()).all()
    return render_template(
        "search_results.html",
        cards=results,
        query=query
    )

@app.route("/delete-selected-cards", methods=["POST"])
def delete_selected_cards():
    if "user_id" not in session:
        return redirect(url_for("login"))
    user_id = session["user_id"]
    card_ids = request.form.getlist("card_ids", type=int)
    if not card_ids:
        return redirect(url_for("all_cards"))
    selected_cards = Card.query.filter(
            Card.id.in_(card_ids),
            Card.user_id == user_id
        ).all()
    for card in selected_cards:
        card.sets.clear()
        db.session.delete(card)
    db.session.commit()
    return redirect(url_for("all_cards"))

@app.route("/cards/all")
def all_cards():
    if "user_id" not in session:
        return redirect(url_for("login"))
    
    user_id = session["user_id"]

    sort = request.args.get("sort", "newest")
    if sort not in ("newest","oldest"):
        sort = "newest"
    
    #validate the page size
    allowed_size = (10, 25, 50)
    try:
        per_page = int(request.args.get("per_page", 10))
    except (TypeError, ValueError):
        per_page = 10
    if per_page not in allowed_size:
        per_page = 10

    query = Card.query.filter_by(user_id=user_id)
    #use card IDs as a temporary proxy
    if sort == "oldest":
        query = query.order_by(Card.id.asc())
    else:
        query = query.order_by(Card.id.desc())

    try:
        page = max(1, int(request.args.get("page", 1)))
    except (TypeError, ValueError):
        page = 1

    cards_page = query.paginate(
        page=page,
        per_page=per_page,
        error_out=False
    )

    card_sets = CardSet.query.filter_by(
         user_id=session["user_id"]
    ).all()

    return render_template(
        "cards.html",
        cards=cards_page.items,
        cards_page=cards_page,
        card_sets=card_sets,
        sort=sort,
        per_page=per_page
        
    )

@app.route("/sets/<int:set_id>")
def view_set(set_id):
    if "user_id" not in session:
        return redirect(url_for("login"))
    card_set = CardSet.query.filter_by(
        id=set_id,
        user_id=session["user_id"]
    ).first_or_404()
    return render_template(
        "set_detail.html",
        card_set=card_set,
        cards=card_set.cards
    )

@app.route("/sets")
def my_sets():
    if "user_id" not in session:
        return redirect(url_for("login"))
    user_id = session["user_id"]
    sort = request.args.get("sort", "newest")
    if sort not in ("newest","oldest"):
        sort = "newest"
    #validate the page size
    allowed_size = (1, 5, 10, 25, 50)
    try:
        per_page = int(request.args.get("per_page", 5))
    except (TypeError, ValueError):
        per_page = 5
    if per_page not in allowed_size:
        per_page = 5

    query = CardSet.query.filter_by(user_id=user_id)
    #use card IDs as a temporary proxy
    if sort == "oldest":
        query = query.order_by(CardSet.id.asc())
    else:
        query = query.order_by(CardSet.id.desc())

    try:
        page = max(1, int(request.args.get("page", 1)))
    except (TypeError, ValueError):
        page = 1

    cards_page = query.paginate(
        page=page,
        per_page=per_page,
        error_out=False
    )
    card_sets = CardSet.query.filter_by(
         user_id=session["user_id"]
    ).all()
    return render_template(
        "sets.html", sort=sort, per_page=per_page,
        cards_page=cards_page, card_sets = card_sets
        
    )
@app.route("/sets/<int:set_id>/remove-card/<int:card_id>", methods=["POST"])
def remove_card_from_set(set_id, card_id):
    if "user_id" not in session:
        return redirect(url_for("login"))
    user_id = session["user_id"]
    # Find a set belonging to the logged-in user
    card_set = CardSet.query.filter_by(
        id=set_id,
        user_id=user_id
    ).first_or_404()
    # Find a flashcard belonging to the logged-in user
    card = Card.query.filter_by(
        id=card_id,
        user_id=user_id
    ).first_or_404()
    # Remove the card from this set only
    if card in card_set.cards:
        card_set.cards.remove(card)
        db.session.commit()
    return redirect(url_for("view_set", set_id=set_id))

@app.route("/add_cards_to_set", methods=["POST"])
def add_cards_to_set():
    # 1. Require login
    if "user_id" not in session:
        return redirect(url_for("login"))
    user_id = session["user_id"]
    # 2. Get the selected set
    set_id = request.form.get("set_id", type=int)
    card_set = CardSet.query.filter_by(
        id=set_id,
        user_id=user_id
    ).first()
    if card_set is None:
        return "Set not found", 404
    # 3. Get the selected card IDs from the submitted form
    card_ids = request.form.getlist("card_ids", type=int)
    if not card_ids:
        return redirect(url_for("my_sets"))
    # 4. Retrieve only cards owned by this user
    selected_cards = Card.query.filter(
        Card.id.in_(card_ids),
        Card.user_id == user_id
    ).all()
    # 5. Add cards to the set, avoiding duplicates
    for card in selected_cards:
        if card not in card_set.cards:
            card_set.cards.append(card)
    # 6. Save the relationship in the database
    db.session.commit()
    return redirect(url_for("my_sets"))

#card_set_cards = db.Table (
#    "card_set_cards",
#    db.Column("card_id", db.Integer, db.ForeignKey("cards.id"), primary_key=True),
#    db.Column("set_id", db.Integer, db.ForeignKey("card_sets.id"), primary_key=True)
#)
#class User(db.Model):
#    __tablename__ = "pot_users"
#    id = db.Column(db.Integer, primary_key=True)
#    username = db.Column(db.String(80), unique=True, nullable=False)
#    password_hash = db.Column(db.String(255), nullable=False)
#    cards = db.relationship("Card", backref="owner")
#    card_sets = db.relationship("CardSet", backref="owner")
#class Card(db.Model):
#    __tablename__ = "cards"
#    id = db.Column(db.Integer, primary_key=True)
#    question = db.Column(db.String(200))
#    answer = db.Column(db.Text)
#    user_id = db.Column(db.Integer, db.ForeignKey("pot_users.id"), nullable=False)
#class CardSet(db.Model):
#    __tablename__ = "card_sets"
#    id = db.Column(db.Integer, primary_key=True)
#    name = db.Column(db.String(100), nullable=False)
#    user_id = db.Column(db.Integer, db.ForeignKey("pot_users.id"), nullable=False)
#    cards = db.relationship("Card", secondary=card_set_cards, backref=db.backref("sets", lazy="select"))
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
@app.route("/create-card", methods=["GET", "POST"])
def create_card():
    if "user_id" not in session:
        return redirect(url_for("login"))
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
##############################################
@app.route("/logout")
def logout():
    session.pop("user", None)
    session.pop("user_id", None)
    session.clear()
    return redirect(url_for("login"))
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
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        _name = request.form.get("username", "").strip()
        _word = request.form.get("password", "")
        if not _word or not _name:
            return render_template(
                    "register.html",
                    error="Please enter both a username and password."
                )
        existing_user = User.query.filter_by(username=_name).first()
        if existing_user:
            return render_template(
                    "register.html",
                    error="That username is already taken."
                    )
        _word_hash = generate_password_hash(_word)
        pappi = User(username=_name, password_hash=_word_hash)
        db.session.add(pappi)
        db.session.commit()
        return redirect(url_for("login"))
    return render_template("register.html")
@app.route("/")
def home():
    if "user_id" not in session:
        return redirect(url_for("login"))
    return render_template("__dashboard__.html")

if __name__ == '__main__':
    app.run(debug=True)
###################################################################################
