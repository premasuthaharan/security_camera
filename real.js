let recordButton = document.getElementById("recordButton");
let recordButtonIcon = recordButton.firstElementChild;
let subtitle = document.getElementById("subtitle");

recordButton.addEventListener("click", startListening);

function startListening() {
		recordButtonIcon.classList.replace("fa-microphone", "fa-circle");
		recordButton.disabled = true;
		
		subtitle.textContent = "Listening...";
		
		let xhr = new XMLHttpRequest();
		xhr.open("GET", "listen", true);
		xhr.onload = processResult;
		xhr.send();
}

function processResult(e) {
		subtitle.textContent = "Result: " + e.target.responseText;
		
		recordButtonIcon.classList.replace("fa-circle", "fa-microphone");
		recordButton.disabled = false;
}
