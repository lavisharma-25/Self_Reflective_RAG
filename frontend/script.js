async function sendQuery() {

    let query = document.getElementById("query").value;

    let chatBox = document.getElementById("chat-box");

    chatBox.innerHTML += `<div class="message user">${query}</div>`;

    document.getElementById("query").value = "";

    let response = await fetch("http://localhost:8000/chat/run", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            question: query
        })
    });

    let data = await response.json();

    chatBox.innerHTML += `<div class="message bot">${data.response.answer}</div>`;
}