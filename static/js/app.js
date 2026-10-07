console.log("Javascript is working")
console.log("And I want a taste")

document.addEventListener("DOMContentLoaded", function () {
	const button = document.getElementById("test-button");
	if (button) {
		button.addEventListener("click", function () {
			alert("Java script is fun");
		});
	}
});

