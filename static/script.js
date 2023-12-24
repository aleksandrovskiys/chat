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
		document.getElementById("login-form").style.display = "none";
		document.getElementById("chat-form").style.display = "block";
	} else {
		document.getElementById("login-form").style.display = "block";
		document.getElementById("chat-form").style.display = "none";
	}
}

function onMessage(event) {
	var messages = document.getElementById("messages");
	var message = document.createElement("li");
	var content = document.createTextNode(event.data);
	message.appendChild(content);
	messages.appendChild(message);
	updateLoggedIn();
}

function sendMessage(event) {
	var input = document.getElementById("messageText");
	const message = {
		type: "message",
		data: { message: input.value },
	};

	ws.send(JSON.stringify(message));
	input.value = "";
	event.preventDefault();
}

var ws = new WebSocket("ws://localhost:5550/websocket/ws");
ws.onmessage = onMessage;
updateLoggedIn();
