function flipCard(card) {
	card.classList.toggle("flipped");
}

document.addEventListener ("DOMContentLoaded", function()
	{
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

		menuButton.addEventListener("click", function()
			{
				if( sidebar.classList.contains("open") ) {
					closeMenu();
				}
				else {
					openMenu();
				}
			}
		);

		closeButton.addEventListener("click", closeMenu);
		overlay.addEventListener("click", closeMenu);

		document.addEventListener("keydown", function(event)
			{
				if (event.key === "Escape" && sidebar.classList.contains("open")) {
					closeMenu();
				}
			}
		);

	}
);

document.addEventListener ("DOMContentLoaded", function ()
	{
		const mode = document.getElementById("selection-mode");
		const message = document.getElementById("selection-message");
		const controls = document.getElementById("add-to-set-controls");
		const deleteButton = document.getElementById("delete-selected-button");
		const deleteControls = document.getElementById("delete-controls");

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
			controls.hidden = !["SELECT", "ALL"].includes(selectionMode);
			deleteControls.hidden = !["delete"].includes(selectionMode);

			if (selectionMode === "delete") {
				message.textContent = "Choose the cards you want to permanently delete.";
			} else {
				message.textContent = "Choose the cards you want to add to a set.";
			}
		}
		mode.addEventListener("change", updateSelectionMode);
		updateSelectionMode();

		deleteButton.addEventListener("click", function (event) {
			const confirmed = window.confirm("Are you sure you want?");
			if (!confirmed){
				event.preventDefault();
			}
		});
	}
);
document.addEventListener ("DOMContentLoaded", function ()
	{
		const monthSelect = document.getElementById("selection-month");
		const tableBody = document.getElementById("table-body");
		const yearInput = document.getElementById("selection-year");
		if (!monthSelect || !tableBody) return;
		function updateCalender(){
			const monthIndex = monthSelect.selectedIndex;
			const year = yearInput ? Number(yearInput.value) : new Date().getFullYear();

			tableBody.replaceChildren();

			const numberOfDays = new Date(year, monthIndex + 1, 0).getDate();

			for(let day = 1; day <= numberOfDays; day++) {
				const row = document.createElement("tr");
				const cell = document.createElement("td");

				cell.textContent = day;
				row.appendChild(cell);
				tableBody.appendChild(row);
			}
		}

		monthSelect.addEventListener("change", updateCalendar);
		if (yearInput) {
			yearInput.addEventListener("change", updateCalendar);
		}
		updateCalender();
	}
);