// SESSION
let session_id = localStorage.getItem("session_id");
if (!session_id) {
    session_id = crypto.randomUUID();
    localStorage.setItem("session_id", session_id);
}

const chatBox = document.getElementById("chat-box");
const queryInput = document.getElementById("query");
const sendBtn = document.getElementById("send-btn");

let isLoading = false;


// FORMAT RESPONSE
function formatAnswer(text) {
    text = text.replace(/\*\*/g, "");

    const lines = text.split(/\n|\r\n/);
    let formatted = "";
    let inList = false;

    lines.forEach(line => {
        line = line.trim();
        if (!line) return;

        const match = line.match(/^(\d+)\.\s+([^\:]+):\s*(.*)$/);

        if (match) {
            if (inList) {
                formatted += "</ul>";
                inList = false;
            }

            formatted += `<strong>${match[1]}. ${match[2]}:</strong> ${match[3]}<br>`;
        } 
        else if (line.startsWith("*")) {
            if (!inList) {
                formatted += "<ul>";
                inList = true;
            }
            formatted += `<li>${line.substring(1).trim()}</li>`;
        } 
        else {
            formatted += line + "<br>";
        }
    });

    if (inList) formatted += "</ul>";
    return formatted;
}


// APPEND MESSAGE
function appendMessage(sender, text) {
    const div = document.createElement("div");
    div.className = `message ${sender}`;
    div.innerHTML = text;
    chatBox.appendChild(div);
    chatBox.scrollTop = chatBox.scrollHeight;
    return div;
}


// LOADING ANIMATION
function startLoadingAnimation(element) {
    let dots = 0;

    return setInterval(() => {
        dots = (dots + 1) % 4;
        element.innerHTML = "Thinking" + ".".repeat(dots);
    }, 500);
}


// TYPING EFFECT
function typeText(element, html) {
    element.innerHTML = "";
    let i = 0;

    const tempDiv = document.createElement("div");
    tempDiv.innerHTML = html;
    const text = tempDiv.innerText;

    function typing() {
        if (i < text.length) {
            element.innerHTML += text.charAt(i);
            i++;
            chatBox.scrollTop = chatBox.scrollHeight;
            setTimeout(typing, 12);
        } else {
            element.innerHTML = html;
        }
    }

    typing();
}


// SEND QUERY
async function sendQuery() {

    if (isLoading) return;

    const query = queryInput.value.trim();
    if (!query) return;

    isLoading = true;
    sendBtn.disabled = true;

    appendMessage("user", query);
    queryInput.value = "";

    const loadingDiv = appendMessage("bot", "<span class='typing'>Thinking...</span>");
    const loadingInterval = startLoadingAnimation(loadingDiv);

    try {
        const res = await fetch("http://localhost:8000/chat/run", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
                question: query,
                session_id: session_id
            })
        });

        const data = await res.json();

        clearInterval(loadingInterval);

        if (data.response && data.response.answer) {
            const formatted = formatAnswer(data.response.answer);
            typeText(loadingDiv, formatted);
        } else {
            loadingDiv.innerHTML = "No response from server.";
        }

    } catch (err) {
        clearInterval(loadingInterval);
        loadingDiv.innerHTML = "Error: Server not reachable.";
        console.error(err);
    } finally {
        isLoading = false;
        sendBtn.disabled = false;
        queryInput.focus();
    }
}


// ENTER KEY
sendBtn.addEventListener("click", sendQuery);

queryInput.addEventListener("keypress", function(e) {
    if (e.key === "Enter") {
        e.preventDefault();
        sendQuery();
    }
});