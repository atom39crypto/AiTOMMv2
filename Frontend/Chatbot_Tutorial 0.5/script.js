document.addEventListener("DOMContentLoaded", function () {
  const promptInput = document.querySelector("#prompt");
  const sendBtn = document.querySelector("#sendBtn");
  const chatContainer = document.querySelector(".chat-container");
  const container = document.querySelector(".container");
  const audioBtn = document.querySelector("#audio-btn");
  const uploadBtn = document.querySelector("#uploadBtn");
  const fileInput = document.querySelector("#fileInput");
  const filePreviewContainer = document.querySelector("#filePreviewContainer");

  let selectedFileDataURL = null;
  let selectedFileName = "";

  // Auto-resize textarea
  if (promptInput) {
    promptInput.setAttribute("style", "height:auto; overflow-y:hidden;");
    promptInput.addEventListener("input", () => {
      promptInput.style.height = "auto";
      promptInput.style.height = promptInput.scrollHeight + "px";
    });
  }

  function createChatBox(html, className) {
    const div = document.createElement("div");
    div.classList.add(className);
    div.innerHTML = html;
    chatContainer.appendChild(div);
    chatContainer.scrollTop = chatContainer.scrollHeight;
    return div;
  }

  function showLoading() {
    const html = `<div class="bubble new">...</div>`;
    return createChatBox(html, "ai-chat-box");
  }

  function formatAIResponse(text) {
    return text
      .replace(/\*\*(.*?)\*\*/g, "<strong>$1</strong>")
      .replace(/```([\s\S]*?)```/g, "<pre><code>$1</code></pre>")
      .replace(/\n/g, "<br>");
  }

  function createCopyButton(textContent) {
    const copyBtn = document.createElement("button");
    copyBtn.className = "copy-btn";
    copyBtn.innerHTML = '<i class="fas fa-copy"></i>';

    copyBtn.addEventListener("click", () => {
      navigator.clipboard.writeText(textContent).then(() => {
        copyBtn.innerHTML = "✓";
        setTimeout(() => {
          copyBtn.innerHTML = '<i class="fas fa-copy"></i>';
        }, 1500);
      });
    });

    return copyBtn;
  }

  function sendMessage() {
    const userMessage = promptInput.value.trim();
    if (!userMessage && !selectedFileDataURL) return;

    container.style.display = "none";

    const messageWrapper = document.createElement("div");
    messageWrapper.classList.add("user-chat-box");

    if (selectedFileDataURL) {
      const fileBlock = document.createElement("div");
      fileBlock.classList.add("chat-file");

      if (selectedFileDataURL.startsWith("data:image")) {
        fileBlock.innerHTML = `<img src="${selectedFileDataURL}" style="max-height: 100px; border-radius: 10px;" />`;
      } else {
        fileBlock.innerHTML = `<i class="fas fa-file-alt fa-2x"></i>`;
      }

      messageWrapper.appendChild(fileBlock);
    }

    if (userMessage) {
      const bubbleWrapper = document.createElement("div");
      bubbleWrapper.classList.add("bubble-wrapper");

      const bubble = document.createElement("div");
      bubble.classList.add("bubble");
      bubble.innerHTML = `<p class="text">${userMessage}</p>`;

      const copyBtn = createCopyButton(userMessage);

      bubbleWrapper.appendChild(bubble);
      bubbleWrapper.appendChild(copyBtn);

      messageWrapper.appendChild(bubbleWrapper);
    }

    chatContainer.appendChild(messageWrapper);
    chatContainer.scrollTop = chatContainer.scrollHeight;

    promptInput.value = "";
    promptInput.style.height = "auto";
    filePreviewContainer.innerHTML = "";

    const filePathToSend = selectedFileName
      ? `E:/python/AI/ATOM/Atom - 8.2/screenshots/${selectedFileName}`
      : null;

    const loadingElement = showLoading();

    eel.get_response(JSON.stringify({ text: userMessage, file_path: filePathToSend }))(function (reply) {
      if (loadingElement) {
        const formatted = formatAIResponse(reply);

        const bubbleWrapper = document.createElement("div");
        bubbleWrapper.classList.add("bubble-wrapper");

        const bubble = document.createElement("div");
        bubble.classList.add("bubble");
        bubble.innerHTML = formatted;

        const copyBtn = createCopyButton(reply);

        bubbleWrapper.appendChild(bubble);
        bubbleWrapper.appendChild(copyBtn);

        loadingElement.innerHTML = "";
        loadingElement.classList.remove("new");
        loadingElement.appendChild(bubbleWrapper);
      }
    });

    selectedFileDataURL = null;
    selectedFileName = "";
  }

  sendBtn.addEventListener("click", sendMessage);

  promptInput.addEventListener("keydown", function (event) {
    if (event.key === "Enter" && !event.shiftKey) {
      event.preventDefault();
      sendMessage();
    }
  });

  const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;

  if (SpeechRecognition) {
    const recognition = new SpeechRecognition();
    recognition.continuous = false;
    recognition.lang = "en-US";
    recognition.interimResults = false;

    audioBtn.addEventListener("click", () => {
      audioBtn.classList.add("mic-active");
      recognition.start();
    });

    recognition.onresult = function (event) {
      const transcript = event.results[0][0].transcript;
      promptInput.value = transcript;
      audioBtn.classList.remove("mic-active");
      sendMessage();
    };

    recognition.onerror = function (event) {
      console.error("Speech recognition error:", event.error);
      audioBtn.classList.remove("mic-active");
    };

    recognition.onend = function () {
      audioBtn.classList.remove("mic-active");
    };
  } else {
    audioBtn.disabled = true;
  }

  uploadBtn.addEventListener("click", () => {
    fileInput.click();
  });

  fileInput.addEventListener("change", async function () {
    const file = this.files[0];
    if (!file) return;

    selectedFileName = file.name;

    const reader = new FileReader();
    reader.onload = function (e) {
      selectedFileDataURL = e.target.result;

      if (file.type.startsWith("image/")) {
        filePreviewContainer.innerHTML = `<img src="${selectedFileDataURL}" style="max-height: 100px; border-radius: 10px;" />`;
      } else {
        filePreviewContainer.innerHTML = `<i class="fas fa-file-alt fa-2x"></i>`;
      }
    };
    reader.readAsDataURL(file);

    const arrayBuffer = await file.arrayBuffer();
    const byteArray = Array.from(new Uint8Array(arrayBuffer));
    eel.save_file_to_disk(byteArray, selectedFileName)();
  });
});
