// 1️⃣ Generate session_id once per user/browser
let session_id = localStorage.getItem("session_id");

if (!session_id) {
    session_id = crypto.randomUUID();
    localStorage.setItem("session_id", session_id);
}

//  Your existing sendQuery function
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
            question: query,
            session_id: session_id
        })
    });

    let data = await response.json();
    chatBox.innerHTML += `<div class="message bot">${data.response.answer}</div>`;
}