ReadMe\

base.html             create_card.html  readme.txt           *set_detail.html
*__dashboard__.html  create_set.html   register.html        *sets.html
*cards.html            login.html        search_results.html

[ * ] cards_dashboard.html///THIS IS THE STARTING PAGE AFTER LOG-IN////////////////////////////////////////////////////////////////////////////////////////////
	My Flashcards
	What would you like to do?
	   - View My Cards
		---- Create Set, CROSS THIS OUT-------------
	   - View My Sets
	Search: "Search all my cards"; "Search".
	* 4 links to new pages:
	   - 1. 'all_cards'
	   - 2. 'create_set'
	   - 3. 'my_sets'
	   - 4. 'search_cards'
	<div class="cards-page">
	<h1>My Flashcards</h1>
	<p>What would you like to do?</p>
	<div class="dashboard-actions">
		<a class="dashboard-button" 
		href="{{ url_for('all_cards') }}">Show All Cards</a>
		<a class="dashboard-button" 
		href="{{ url_for('create_set') }}">Create Set</a>
		<a class="dashboard-button" 
		href="{{ url_for('my_sets') }}">View My Sets</a>
	</div>
	
	<form 
		action="{{ url_for('search_cards') }}"
		method="GET"
		class="card-search"
	>
		<label for="q">Search all my cards</label>
		<input
			type="search"
			id="q"
			name="q"
			placeholder="Search questions and answers..."
		>

		<button type="submit" class="remove-set-button">Search</button>
	</form>
</div>

[ 1 ] cards.html///////////////////////////////////////////////////////////// 
FROM: dashboard: 'Show All Cards' -- url_for('all_cards')
TO:
<div class="cards-page">

	<p><a href="{{ url_for('create_card') }}">
			+ Create a Flashcard     </a></p>

	<form id="card-selection-form" method="POST"
		action="{{ url_for('add_cards_to_set') }}">

		<label for="selection-mode">Select cards:</label>
		<select id="selection-mode" name="selection_mode">
			<option value="NONE">None</option>
			<option value="SELECT">Select</option>
			<option value="ALL">Select All</option>
			<option value="delete">Delete</option>
		</select>

		<p id="selection-message" hidden>
			Choose the cards you want to add to a set.</p>

		<div class="cards-grid">
		{% for card in cards %}
		<div class="card-item">
			<label class="card-select" hidden>
			<input
				type="checkbox"
				class="card-checkbox"
				name="card_ids"
				value="{{ card.id }}"
			>
				Select Card</label>

			<div class="flashcard" onclick="flipCard(this)">
				<div class="flashcard-inner">
					<div class="flashcard-front">
						<h3>Question</h3>
						<p>{{ card.question }}</p>
						<small>Click to reveal answer
						</small>
					</div>
					<div class="flashcard-back">
						<h3>Answer</h3>
						<p>{{ card.answer }}</p>
						<small>Click to return</small>
					</div>
				</div>
			</div>
		</div>			
		{% else %}
			<p>You haven't created any flashcards yet.</p>
		{% endfor %}
		<br><br>
		</div>

		<div id="add-to-set-controls" hidden>
			<br>
			<br>
			<label for="set-id">Choose a set:</label>
			<select id="set-id" name="set_id" required>
				<option value="">-- Choose a set --</option>
				{% for card_set in card_sets %}
					<option value="{{ card_set.id }}">
					{{ card_set.name }}
				</option>
				{% endfor %}
			</select>

			<button type="submit" id="confirm-selection" 
				class="remove-set-button">
				Add Selected Cards to Set
			</button>
		</div>
	
	</form>
</div>

[ 3 ] sets.html//////////////////////////////////////////////////////////////
FROM: dashboard: 'View My Sets', url_for('my_sets')
TO: 
    My Sets 
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
[ 3A ] set_detail.html//////////////////////////////////////////////////////////
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





