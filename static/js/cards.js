	document.addEventListener (
		"DOMContentLoaded", 
		function() {
			
			const menuButton = document.getElementById("menu-toggle");
			

			const sidebar = document.getElementById("sidebar");
			const overlay = document.getElementById("sidebar-overlay");
			const closeButton = document.getElementById("sidebar-close");

			function openMenu() {
				sidebar.classList.add("open");
				overlay.hidden=false;
				document.body.classList.add("menu-open");
				menuButton.setAttribute("aria-expanded", "true");
				menuButton.setAttribute("aria-label", "Close navigation menu");
				sidebar.setAttribute("aria-hidden", "false");
				closeButton.focus();

			}

			function closeMenu() {
				sidebar.classList.remove("open");
				overlay.hidden = true;
				document.body.classList.remove("menu-open");
				menuButton.setAttribute("aria-expanded", "false");
				menuButton.setAttribute("aria-label", "Open navigation menu");
				sidebar.setAttribute("aria-hidden", "true");

				menuButton.focus();
			}
			menuButton.addEventListener("click", 
				function() {
					if(sidebar.classList.contains("open")) {
						closeMenu();
					} else {
						openMenu();
					}
				}
			);

			closeButton.addEventListener("click", closeMenu);
			overlay.addEventListener("click", closeMenu);

			document.addEventLIstener(
				"keydown",
				function(event) {
					if (event.key === "Escape" && sidebar.classList.contains("open")) {
						closeMenu();
					}
				}
			);
		}
	);
			

	function flipCard(card) {
		card.classList.toggle("flipped");
	}

	document.addEventListener (
		"DOMContentLoaded", 
		function () {
		
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

		}
	);
