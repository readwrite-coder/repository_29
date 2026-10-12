
	function flipCard(card) {
		card.classList.toggle("flipped");
	}

	document.addEventListener("DOMContentLoaded", function () {
		const mode = document.getElementById("selection-mode");
		const message = document.getElementById("selection-message");
		
		const continueButton = document.getElementById("confirm-selection");    
		const deleteOption = document.getElementById("del-button");

		const checkboxes = document.querySelectorAll(".card-checkbox");
		const labels = document.querySelectorAll(".card-select");
		
		function updateSelectionMode() {
			
			const selectionMode = mode.value;
			
			checkboxes.forEach( function (checkbox,index) {
				labels[index].hidden = selectionMode === "NONE";
				checkbox.checked = selectionMode == "ALL";
			});
			
			message.hidden = selectionMode === "NONE";
			
			continueButton.hidden = selectionMode === "NONE";

			/*deleteOption.hidden = selectionMode === "NONE";*/
			
			
		}

			mode.addEventListener("change", updateSelectionMode);

			continueButton.addEventListener("click", function() {
				const selectedCards = Array.from(checkboxes).filter(function (checkbox) {
					return checkbox.checked;
				})
					.map(function (checkbox) {
						return checkbox.value;
					});
				console.log("Selected card IDs:", selectedCards);
			});

                        updateSelectionMode();
		});



