	function flipCard(card) {
		card.classList.toggle("flipped");
	}

	document.addEventListener("DOMContentLoaded", function () {
		
		const mode = document.getElementById("selection-mode");
		const message = document.getElementById("selection-message");
		const controls = document.getElementById("add-to-set-controls");
		const checkboxes = document.querySelectorAll(".card-checkbox");
		const labels = document.querySelectorAll(".card-select");

		function updateSelectionMode() {
			const selectionMode = mode.value;

			checkboxes.forEach(function (checkbox, index) {
				labels[index].hidden = selectionMode === "NONE";

				if (selectionMode === "ALL") {
					checkbox.checked = true;
				} else if (selectionMode === "NONE") {
					checkbox.checked = false;
				}
			});

			message.hidden = selectionMode === "NONE";
			controls.hidden = selectionMode === "NONE";
		}

		mode.addEventListener("change", updateSelectionMode);
		updateSelectionMode();

	});
