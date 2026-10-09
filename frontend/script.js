const input =
    document.getElementById("user-input");

const home =
    document.getElementById("home");

const chatArea =
    document.getElementById("chat-area");


// ====================================
// SEND MESSAGE
// ====================================

async function sendMessage() {

    const message =
        input.value.trim();


    if (message === "") {

        return;

    }


    // Hide home

    home.style.display = "none";


    // Show chat

    chatArea.classList.add("active");


    // Add user message

    addMessage(
        message,
        "user"
    );


    // Clear input

    input.value = "";


    // Thinking message

    const thinking =
        addMessage(
            "Thinking...",
            "bot"
        );


    try {

        const response =
            await fetch(
                "http://127.0.0.1:8000/chat",
                {

                    method: "POST",

                    headers: {

                        "Content-Type":
                            "application/json"

                    },

                    body: JSON.stringify({

                        message: message

                    })

                }
            );


        if (!response.ok) {

            throw new Error(
                "Server error"
            );

        }


        const data =
            await response.json();


        // Remove thinking

        thinking.remove();


        // Show AI answer

        addMessage(
            data.reply,
            "bot"
        );


    }

    catch (error) {

        thinking.remove();


        addMessage(

            "❌ Cannot connect to Offline AI.\n\n" +

            "Please make sure FastAPI and Ollama are running.",

            "bot"

        );


        console.error(error);

    }

}


// ====================================
// ADD MESSAGE
// ====================================

function addMessage(
    message,
    type
) {

    const messageDiv =
        document.createElement("div");


    messageDiv.className =
        "message " + type;


    const content =
        document.createElement("div");


    content.className =
        "message-content";


    content.textContent =
        message;


    messageDiv.appendChild(
        content
    );


    chatArea.appendChild(
        messageDiv
    );


    chatArea.scrollTop =
        chatArea.scrollHeight;


    return messageDiv;

}


// ====================================
// NEW CHAT
// ====================================

function newChat() {

    chatArea.innerHTML = "";

    chatArea.classList.remove(
        "active"
    );

    home.style.display = "flex";

    input.value = "";

    input.focus();

}


// ====================================
// SUGGESTION
// ====================================

function useSuggestion(text) {

    input.value = text;

    input.focus();

    sendMessage();

}


// ====================================
// PROGRAM
// ====================================

function showProgram() {

    useSuggestion(
        "Explain programming in simple words."
    );

}


// ====================================
// RECENT
// ====================================

function showRecent() {

    addMessage(
        "Recent chats are stored in this session.",
        "bot"
    );

}


// ====================================
// PINS
// ====================================

function showPins() {

    addMessage(
        "Pinned chats will appear here.",
        "bot"
    );

}


// ====================================
// ENTER KEY
// ====================================

input.addEventListener(
    "keydown",
    function(event) {

        if (
            event.key === "Enter" &&
            !event.shiftKey
        ) {

            event.preventDefault();

            sendMessage();

        }

    }
);