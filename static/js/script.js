const toggleSidebarBtn = document.getElementById("toggleSidebar");
const sidebar = document.getElementById("sidebar");
const mainContent = document.getElementById("main-content");

const conversationHistory = document.getElementById("conversation-history");
conversationHistory.innerHTML = "";

const botMessages = [
  "Olá, eu sou um chatbot projetado para responder e resolver suas dúvidas sobre vacas, bois e outros temas relacionados!",
  "Olá, como posso ajudá-lo?",
  "Sim, entendi. Posso ajudá-lo com isso?",
  "Não entendi. Pode explicar melhor?",
  "Ok, vou verificar isso.",
  "Sim, é possível. Vou ajudá-lo a resolver isso."
];

toggleSidebarBtn.addEventListener("click", () => {
    if (sidebar.style.width === "0px" || sidebar.style.width === "0") {
        sidebar.style.width = "250px";
        mainContent.style.marginLeft = "250px";
        toggleSidebarBtn.textContent = "Hide Sidebar";
        toggleSidebarBtn.innerHTML = '<i class="bi bi-list"></i>';
    } else {
        sidebar.style.width = "0";
        mainContent.style.marginLeft = "0";
        toggleSidebarBtn.textContent = "Show Sidebar";
        toggleSidebarBtn.innerHTML = '<i class="bi bi-list"></i>';
    }
});

document.getElementById("sendBtn").addEventListener("click", () => {
    const chatInput = document.getElementById("chat-input");
    const chatBox = document.getElementById("chat-box");

    const message = chatInput.value;
    if (message.trim()) {
        const messageElement = document.createElement("div");
        messageElement.textContent = message;
        messageElement.className = "sent-message";
        messageElement.style ="word-wrap: break-word;";
        chatBox.appendChild(messageElement);
        chatInput.value = "";

        const botMessage = botMessages[Math.floor(Math.random() * botMessages.length)];

        const botMessageElement = document.createElement("div");
        botMessageElement.textContent = botMessage;
        botMessageElement.className = "received-message";
        botMessageElement.style ="word-wrap: break-word;";
        chatBox.appendChild(botMessageElement);

        const conversationItem = document.createElement("li");
        conversationItem.textContent = `Você: ${message} | Bot: ${botMessage}`;
        conversationHistory.appendChild(conversationItem);
    }
});

