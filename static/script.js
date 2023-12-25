let loggedIn = false;

function login(event) {
	username = document.getElementById("username").value;
	const message = {
		type: "login",
		data: { username },
	};

	ws.send(JSON.stringify(message));

	username.input = "";

	event.preventDefault();
}

function updateLoggedIn() {
	if (loggedIn) {
		document.getElementById("login-block").style.display = "none";
		document.getElementById("chat-block").style.display = "block";
		document.getElementById("input-message-block").style.display = "block";
	} else {
		document.getElementById("login-block").style.display = "block";
		document.getElementById("chat-block").style.display = "none";
		document.getElementById("input-message-block").style.display = "none";
	}
}

function onMessage(event) {
	const data = JSON.parse(event.data);
	switch (data.response_type) {
		case "successful_login":
			loggedIn = true;
			updateLoggedIn();
			break;
		case "message":
			let messages = document.getElementById("messages-container");
			let chatBlock = document.getElementById("chat-block");
			let message = getMessageDiv(data.message, data.data.author.username);
			messages.appendChild(message);
			chatBlock.scrollTop = chatBlock.scrollHeight;
			break;

		default:
			break;
	}
}

function sendMessage(event) {
	let input = document.getElementById("messageText");
	const message = {
		type: "message",
		data: { message: input.value },
	};

	ws.send(JSON.stringify(message));
	input.value = "";
	event.preventDefault();
}

function getMessageDiv(message, username) {
	let temp = document.getElementsByTagName("template")[0];
	let clon = temp.content.cloneNode(true);
	clon.querySelector(".message").textContent = message;
	clon.querySelector(".username").textContent = username || "Anonymous";

	return clon;
}

let ws = new WebSocket("ws://localhost:5550/websocket/ws");
ws.onmessage = onMessage;
updateLoggedIn();
