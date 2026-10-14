ReadMe

[ 3 ] cards_dashboard.html
       

[ 4 ] set_detail.html//////////////////////////////////////////////////////////
"/sets/11"
- [Set Name]
- 0 cards in this set
- Back to My Sets
- This set is empty. Add some flashcards to get started!
<div class="cards-page">
	<h1>[{{ card_set.name }}]</h1>
	<p>{{ cards|length }} cards in this set</p>
	<p>
	<a href="{{ url_for('my_sets') }}">Back to My Sets</a>
	</p>

<div class="cards-grid">
	
	{% for card in cards %}
	<div class="card-item">
		<div class="flashcard" onclick="flipCard(this)">
			<div class="flashcard-inner">

				<div class="flashcard-front">
					<h3>Question</h3>
					<p>{{ card.question }}</p>
					<small>Click to reveal answer</small>
				</div>
				<div class="flashcard-back">
					<h3>Answer</h3>
					<p>{{ card.answer }}</p>
					<small>Click to return</small>
				</div>
			</div>
		</div>
		<form
			method="POST"
			action="{{ url_for('remove_card_from_set',
				set_id=card_set.id,
				card_id=card.id) }}"
			onsubmit="return confirm(
			'Remove this card from the set?');"
			>
			
			<button type="submit" class="remove-set-button">
				Remove from Set
			</button>
		</form>
	</div>
	{% else %}
		<p>This set is empty. Add some flashcards to get started!</p>
	{% endfor %}
	
</div>
</div>

	<script>
	function flipCard(card) {
		card.classList.toggle("flipped");
[ 3 ] sets.html//////////////////////////////////////////////////////////////
FROM: dashboard: 'View My Sets'
To: My Sets 
    { + Create a Set } 
    (set -- no. cards) 
    (set -- no. cards)
<div class="cards-page">
	<h1>My Sets</h1>
	<a class="create-button" href="{{ url_for('create_set') }}">
		+ Create a Set
	</a>
		{
		@app.route("/sets/create", methods=["GET", "POST"])
		def create_set():
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
		}
	{% for card_set in sets %}
		<p>
		<a href="{{ url_for("view_set", set_id=card_set.id) }}">
				{{ card_set.name }}	
		</a>
			-- [{{ card_set.cards|length }} cards]
		</p>
		{
		@app.route("/sets/<int:set_id>")
		def view_set(set_id):
		card_set = CardSet.query.filter_by(
        		id=set_id,
        		user_id=session["user_id"]
    			).first_or_404()

    		return render_template(
        		"set_detail.html", 
        		card_set=card_set,
        		cards=card_set.cards
   		 	)
		}
	{% else %}
		<p>You haven't created any sets yet.</p>
	{% endfor %}

[ 1 ] base.html



